import requests
import streamlit as st

API_URL_INGREDIENTS = "https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"

def fetch_all_ingredients():
    """
    Fetches all ingredients from TheCocktailDB API.
    """
    try:
        response = requests.get(API_URL_INGREDIENTS)
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            if 'drinks' in data:
                # Extract the ingredient names
                return [ingredient['strIngredient1'] for ingredient in data['drinks']]
            else:
                st.error("No ingredients found.")
                return []
        else:
            st.error(f"Error {response.status_code}: Failed to fetch ingredients from TheCocktailDB")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Request exception: {e}")
        return []



API_URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="

def fetch_cocktails_by_ingredient(ingredient):
    """
    Fetches cocktails from TheCocktailDB API for a single ingredient.
    """
    api_url = f"{API_URL_BASE}{ingredient}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            if 'drinks' in data:
                return data['drinks']  # Return the list of drinks
            else:
                return []  # No drinks found for this ingredient
        else:
            st.error(f"Error {response.status_code}: Failed to fetch data from TheCocktailDB")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Request exception: {e}")
        return []
