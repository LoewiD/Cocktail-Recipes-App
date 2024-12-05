import requests
import string
import csv
import time
from openai import OpenAI

# set the API key for GPT-4o
client = OpenAI(
    api_key='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')

MODEL = "gpt-4o" #selecting a model for data reading and generation


def safe_str(value):
    """Helper function to safely convert values to strings, replacing None with an empty string."""
    return "" if value is None else str(value)


def generate_feature_scores(cocktail_name, ingredients, glass_type, instruction_length, preparation_complexity):        #defining the goal of the OpenAI API
    """
    Use GPT-4o to generate feature scores based on cocktail characteristics.

    Parameters:
        cocktail_name (str): The name of the cocktail.
        ingredients (list of str): List of ingredients used in the cocktail.
        glass_type (str): The type of glass in which the cocktail is served.
        instruction_length (int): Length of the preparation instructions.
        preparation_complexity (int): Complexity score based on the number of keywords in the instructions.

    Returns:
        dict: A dictionary of feature scores that will be used for training the ML model.
    """
    # Construct the messages prompt for the chat model
    messages = [
        {"role": "system", "content": "You are an expert in evaluating cocktails for difficulty based on their characteristics."},      #prompt for data generation (OpenAI API)
        {
            "role": "user",
            "content": f"""
            Given the following cocktail:
            - Name: {cocktail_name}
            - Ingredients: {', '.join(ingredients)}
            - Glass type: {glass_type}
            - Instruction length: {instruction_length} words
            - Preparation complexity score: {preparation_complexity}

            Please provide ratings on the following features that contribute to the difficulty level of preparing this cocktail:
            - Ingredient Complexity (0-10): How complex are the ingredients to handle and combine?
            - Instruction Complexity (0-10): How difficult are the preparation steps?
            - Tool Complexity (0-10): How complex are the tools needed for preparation?
            - Glass Type Complexity (0-10): How difficult is it to handle and serve in the specified glass type?

            Respond only with the scores in the following format:
            Ingredient Complexity: [0-10]
            Instruction Complexity: [0-10]
            Tool Complexity: [0-10]
            Glass Type Complexity: [0-10]
            """
        }
    ]

    try:
        # make the request to GPT-4o
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        response_text = completion.choices[0].message.content.strip()
        print(f"Response from GPT-4o for '{cocktail_name}':\n{response_text}\n")

        # parsing the response to get the feature scores
        scores = {}
        try:
            for line in response_text.split('\n'):
                key, value = line.split(":")
                scores[key.strip()] = int(value.strip())

            return scores
        except Exception as parse_error:
            print(f"Error parsing response for '{cocktail_name}': {parse_error}")       #exception case if an error occurs during parsing
            return {
                "Ingredient Complexity": 5,     #default values if error occurs
                "Instruction Complexity": 5,
                "Tool Complexity": 5,
                "Glass Type Complexity": 5
            }

    except Exception as e:
        print(f"Error generating feature scores for '{cocktail_name}': {e}")        #exception case if error occurs during data generation
        return {
            "Ingredient Complexity": 5,     #default set to moderate if error occurs
            "Instruction Complexity": 5,
            "Tool Complexity": 5,
            "Glass Type Complexity": 5
        }


def fetch_cocktails():          #fetching cocktail daty from cocktail database for generation of machine learning dataset
    """
    Fetch cocktail data from TheCocktailDB API and save it to a CSV file.

    Fetches cocktails for each letter of the alphabet, extracts important fields, and saves
    them into a CSV file. Adds relevant features for machine learning.
    """
    base_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f="
    cocktails = []


    for letter in string.ascii_lowercase:           # attempt to fetch cocktails for each letter of the alphabet
        response = None
        try:
            response = requests.get(base_url + letter, timeout=10)  # add timeout for request (minimize potential errors due to API requests overload)
            response.raise_for_status()  # raise an error for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for letter '{letter}': {e}")
            continue  # skip to the next letter if there's an error

        if response.status_code == 200:     #check status if OK (200)
            data = response.json()
            if data and data.get("drinks"):
                cocktails.extend(data["drinks"])
                print(f"Fetched data for letter '{letter}': {len(data['drinks'])} drinks.")     #print current letter for visualization of progress
            else:
                print(f"No drinks found for letter '{letter}'.")
        else:
            print(f"Unexpected status code {response.status_code} for letter '{letter}'.")

    # if no cocktails were fetched, print an error and exit
    if not cocktails:
        print("No cocktail data fetched. Please check your network connection and API availability.")
        return

    # define CSV header with extended ingredients, measurements, and new features
    csv_header = [
        "idDrink", "strDrink", "strCategory", "strAlcoholic", "strGlass",
        "strInstructions", "strIngredient1", "strIngredient2", "strIngredient3", "strIngredient4", "strIngredient5",
        "strIngredient6", "strIngredient7", "strIngredient8", "strIngredient9", "strIngredient10", "strIngredient11",
        "strIngredient12", "strIngredient13", "strIngredient14", "strIngredient15",
        "strMeasure1", "strMeasure2", "strMeasure3", "strMeasure4", "strMeasure5",
        "strMeasure6", "strMeasure7", "strMeasure8", "strMeasure9", "strMeasure10",
        "strMeasure11", "strMeasure12", "strMeasure13", "strMeasure14", "strMeasure15",
        "num_ingredients", "instruction_length", "num_measurements", "preparation_complexity",
        "ingredient_complexity", "instruction_complexity", "tool_complexity", "glass_type_complexity"
    ]

    try:
        # write fetched cocktail data to a CSV file
        with open("cocktails_data.csv", "w", newline="", encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_header)

            for cocktail in cocktails:
                # extract up to 15 ingredients and measures
                ingredients = [safe_str(cocktail.get(f"strIngredient{i}")) for i in range(1, 16)]
                measures = [safe_str(cocktail.get(f"strMeasure{i}")) for i in range(1, 16)]

                # ensure ingredients and measurements are always 15 elements long
                # if there are fewer ingredients or measures, fill with empty strings
                ingredients = ingredients + [""] * (15 - len(ingredients))
                measures = measures + [""] * (15 - len(measures))

                # count the number of ingredients and measurements used
                num_ingredients = len([ing for ing in ingredients if ing])
                num_measurements = len([meas for meas in measures if meas])

                # calculate the length of the instructions in words
                instruction_length = len(cocktail.get("strInstructions", "").split())

                # calculate preparation complexity based on specific keywords in the instructions
                complex_keywords = ['shake', 'blend', 'layer', 'strain', 'stir', 'muddle']
                preparation_complexity = sum(1 for keyword in complex_keywords if keyword in cocktail.get("strInstructions", "").lower())

                # generate feature scores using GPT-4o
                feature_scores = generate_feature_scores(
                    cocktail.get("strDrink", ""), ingredients, cocktail.get("strGlass", ""), instruction_length, preparation_complexity
                )

                # create a row with all columns
                row = [
                    safe_str(cocktail.get("idDrink")),
                    safe_str(cocktail.get("strDrink")),
                    safe_str(cocktail.get("strCategory")),
                    safe_str(cocktail.get("strAlcoholic")),
                    safe_str(cocktail.get("strGlass")),
                    safe_str(cocktail.get("strInstructions"))
                ]

                # add ingredients and measurements
                row += ingredients
                row += measures

                # add calculated features and generated feature scores
                row += [
                    num_ingredients,
                    instruction_length,
                    num_measurements,
                    preparation_complexity,
                    feature_scores.get("Ingredient Complexity"),
                    feature_scores.get("Instruction Complexity"),
                    feature_scores.get("Tool Complexity"),
                    feature_scores.get("Glass Type Complexity")
                ]

                # write row to CSV
                writer.writerow(row)

                print(f"Writing data for cocktail: {cocktail.get('strDrink', 'Unknown')}")


                # to avoid rate limits, add a slight delay between requests to GPT-4o (if error occurs during running, avoid unnecessary requests)
                time.sleep(1)

        print("Data successfully saved to cocktails_data.csv")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")


# run the function
if __name__ == "__main__":
    fetch_cocktails()
