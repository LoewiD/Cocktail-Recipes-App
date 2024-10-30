import requests
import string
import csv
import time
from openai import OpenAI

# Set the API key for GPT-4o
client = OpenAI(api_key='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')

MODEL = "gpt-4o"

def safe_str(value):
    """Helper function to safely convert values to strings, replacing None with an empty string."""
    return "" if value is None else str(value)

def generate_motif_popularity_scores(cocktail_name, ingredients, glass_type):
    """
    Use GPT-4o to generate motif and popularity scores based on cocktail characteristics.

    Parameters:
        cocktail_name (str): The name of the cocktail.
        ingredients (list of str): List of ingredients used in the cocktail.
        glass_type (str): The type of glass in which the cocktail is served.

    Returns:
        tuple: (motif_casual, motif_formal, motif_party, motif_romantic,
                popularity_default, popularity_casual, popularity_formal, popularity_party, popularity_romantic)
    """
    # Construct the messages prompt for the chat model
    messages = [
        {"role": "system", "content": "You are an expert in evaluating cocktails for different types of occasions."},
        {
            "role": "user",
            "content": f"""
            Given the following cocktail:
            - Name: {cocktail_name}
            - Ingredients: {', '.join(ingredients)}
            - Glass type: {glass_type}

            Please provide ratings on the following motifs and popularity scores in a clear, concise format:
            Motif Casual (0-10)
            Motif Formal (0-10)
            Motif Party (0-10)
            Motif Romantic (0-10)
            Overall Popularity (0-100)
            Popularity for Casual setting (0-100)
            Popularity for Formal setting (0-100)
            Popularity for Party setting (0-100)
            Popularity for Romantic setting (0-100)

            Respond only with the scores in the following exact format:
            Motif Casual: [0-10]
            Motif Formal: [0-10]
            Motif Party: [0-10]
            Motif Romantic: [0-10]
            Popularity Default: [0-100]
            Popularity Casual: [0-100]
            Popularity Formal: [0-100]
            Popularity Party: [0-100]
            Popularity Romantic: [0-100]
            """
        }
    ]

    try:
        # Make the request to GPT-4o
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        response_text = completion.choices[0].message.content.strip()
        print(f"Response from GPT-4o for '{cocktail_name}':\n{response_text}\n")

        # Parsing the response to get scores
        scores = {}
        try:
            for line in response_text.split('\n'):
                key, value = line.split(":")
                scores[key.strip()] = int(value.strip())

            return (
                scores.get("Motif Casual", 5),
                scores.get("Motif Formal", 5),
                scores.get("Motif Party", 5),
                scores.get("Motif Romantic", 5),
                scores.get("Popularity Default", 50),
                scores.get("Popularity Casual", 50),
                scores.get("Popularity Formal", 50),
                scores.get("Popularity Party", 50),
                scores.get("Popularity Romantic", 50)
            )
        except Exception as parse_error:
            print(f"Error parsing response for '{cocktail_name}': {parse_error}")
            return (5, 5, 5, 5, 50, 50, 50, 50, 50)

    except Exception as e:
        print(f"Error generating motif scores for '{cocktail_name}': {e}")
        return (5, 5, 5, 5, 50, 50, 50, 50, 50)

def fetch_cocktails():
    """
    Fetch cocktail data from TheCocktailDB API and save it to a CSV file.

    Fetches cocktails for each letter of the alphabet, extracts important fields, and saves
    them into a CSV file. Adds realistic motif and popularity scores using GPT-4o.
    """
    base_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f="
    cocktails = []

    # Attempt to fetch cocktails for each letter of the alphabet
    for letter in string.ascii_lowercase:
        response = None
        try:
            response = requests.get(base_url + letter, timeout=10)  # Add timeout for request
            response.raise_for_status()  # Raise an error for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for letter '{letter}': {e}")
            continue  # Skip to the next letter if there's an error

        if response.status_code == 200:
            data = response.json()
            if data and data.get("drinks"):
                cocktails.extend(data["drinks"])
                print(f"Fetched data for letter '{letter}': {len(data['drinks'])} drinks.")
            else:
                print(f"No drinks found for letter '{letter}'.")
        else:
            print(f"Unexpected status code {response.status_code} for letter '{letter}'.")

    # If no cocktails were fetched, print an error and exit
    if not cocktails:
        print("No cocktail data fetched. Please check your network connection and API availability.")
        return

    # Define CSV header with extended ingredients and measurements
    csv_header = [
        "idDrink", "strDrink", "strCategory", "strAlcoholic", "strGlass", 
        "strInstructions", "strIngredient1", "strIngredient2", "strIngredient3", "strIngredient4", "strIngredient5",
        "strIngredient6", "strIngredient7", "strIngredient8", "strIngredient9", "strIngredient10", "strIngredient11",
        "strIngredient12", "strIngredient13", "strIngredient14", "strIngredient15", 
        "strMeasure1", "strMeasure2", "strMeasure3", "strMeasure4", "strMeasure5",
        "strMeasure6", "strMeasure7", "strMeasure8", "strMeasure9", "strMeasure10",
        "strMeasure11", "strMeasure12", "strMeasure13", "strMeasure14", "strMeasure15",
        "Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic", 
        "Popularity_Default", "Popularity_Casual", "Popularity_Formal", "Popularity_Party", "Popularity_Romantic"
    ]

    try:
        # Write fetched cocktail data to a CSV file
        with open("cocktails_data.csv", "w", newline="", encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_header)
            
            for cocktail in cocktails:
                # Extract up to 15 ingredients and measures
                ingredients = [safe_str(cocktail.get(f"strIngredient{i}")) for i in range(1, 16)]
                measures = [safe_str(cocktail.get(f"strMeasure{i}")) for i in range(1, 16)]

                # Ensure ingredients and measurements are always 15 elements long
                # If there are fewer ingredients or measures, pad with empty strings
                ingredients = ingredients + [""] * (15 - len(ingredients))
                measures = measures + [""] * (15 - len(measures))

                # Create a row with empty placeholders for all columns (45 columns)
                row = [""] * 45

                # Fill in the fixed columns for basic cocktail info (positions 0 to 5)
                row[0:6] = [
                    safe_str(cocktail.get("idDrink")),
                    safe_str(cocktail.get("strDrink")),
                    safe_str(cocktail.get("strCategory")),
                    safe_str(cocktail.get("strAlcoholic")),
                    safe_str(cocktail.get("strGlass")),
                    safe_str(cocktail.get("strInstructions"))
                ]

                # Fill in ingredients (positions 6 to 20)
                row[6:21] = ingredients

                # Fill in measures (positions 21 to 35)
                row[21:36] = measures

                # Generate realistic motif and popularity scores using GPT-4o
                scores = generate_motif_popularity_scores(
                    cocktail.get("strDrink", ""), ingredients, cocktail.get("strGlass", "")
                )

                # Fill in motif and popularity scores in fixed positions (positions 36 to 44)
                row[36:45] = [safe_str(score) for score in scores]

                # Write row to CSV
                writer.writerow(row)

                # To avoid rate limits, add a slight delay between requests to GPT-4o
                time.sleep(1)

        print("Data successfully saved to cocktails_data.csv")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

# Run the function
if __name__ == "__main__":
    fetch_cocktails()
