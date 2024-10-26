import requests
import string
import csv
import random
import time

def fetch_cocktails():
    """
    Fetch cocktail data from TheCocktailDB API and save it to a CSV file.
    
    Fetches cocktails for each letter of the alphabet, extracts important fields, and saves
    them into a CSV file. Also adds random motif values and popularity scores.
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
                ingredients = [cocktail.get(f"strIngredient{i}", "") for i in range(1, 16)]
                measures = [cocktail.get(f"strMeasure{i}", "") for i in range(1, 16)]

                # Generate random motif and popularity values
                motif_casual = random.randint(0, 10)
                motif_formal = 10 - motif_casual
                motif_party = random.randint(0, 10)
                motif_romantic = 10 - motif_party
                popularity_default = random.randint(1, 100)
                popularity_casual = random.randint(1, 100)
                popularity_formal = random.randint(1, 100)
                popularity_party = random.randint(1, 100)
                popularity_romantic = random.randint(1, 100)

                # Create a row for each cocktail
                row = [
                    cocktail.get("idDrink", ""), cocktail.get("strDrink", ""), cocktail.get("strCategory", ""), 
                    cocktail.get("strAlcoholic", ""), cocktail.get("strGlass", ""), cocktail.get("strInstructions", "")
                ] + ingredients + measures + [
                    motif_casual, motif_formal, motif_party, motif_romantic,
                    popularity_default, popularity_casual, popularity_formal, popularity_party, popularity_romantic
                ]

                # Write row to CSV
                writer.writerow(row)

        print("Data successfully saved to cocktails_data.csv")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

# Run the function
if __name__ == "__main__":
    fetch_cocktails()
