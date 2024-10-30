#data_fetch.py
import requests
import streamlit as st

# API URLs used for fetching ingredients, cocktails based on ingredients, and detailed cocktail information.
API_URL_INGREDIENTS = "https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"  # Endpoint to fetch all available ingredients
API_URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="  # Endpoint to fetch cocktails based on an ingredient
API_URL_LOOKUP = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i="  # Endpoint to fetch detailed cocktail info based on cocktail ID

# This function fetches all available ingredients from TheCocktailDB API.
def fetch_all_ingredients():
    try:
        # Send a GET request to the API URL for ingredients
        response = requests.get(API_URL_INGREDIENTS, timeout=10)

        # Check if the request was successful (HTTP status code 200 means OK/Good)
        if response.status_code == 200:
            # Parse the JSON response from the API
            data = response.json()  # The API response is a JSON object (JSON = standardized text-format readable by Python)

            # Check if the 'drinks' key is present in the response data
            if 'drinks' in data:
                # Return a list of ingredient names by extracting 'strIngredient1' for each ingredient
                return [ingredient['strIngredient1'] for ingredient in data['drinks']]  # list comprehension to generate new list of all the ingredients
            else:
                # If no drinks were found, display an error message in Streamlit
                st.error("No ingredients found in the response.")
                return []
        else:
            # If the request was not successful, display an error message with the status code
            st.error(f"Error {response.status_code}: Failed to fetch ingredients from TheCocktailDB")
            return []

    # Handle network-related errors (timeout, DNS issues, etc.)
    except requests.exceptions.RequestException as e:
        # Display an error message in Streamlit with details about the exception
        st.error(f"Request exception: {e}")
        return []

# This function fetches cocktails from TheCocktailDB API for a single ingredient.
def fetch_cocktails_by_ingredient(ingredient):
    # Construct the full API URL by appending the ingredient to the base URL
    api_url = f"{API_URL_BASE}{ingredient}"

    try:
        # Send a GET request to the API URL to fetch cocktails containing the specified ingredient
        response = requests.get(api_url, timeout=10)

        # Check if the request was successful (HTTP status code 200 means OK/good)
        if response.status_code == 200:
            # Parse the JSON response from the API
            data = response.json()  # The API response is a JSON object --> converted into Python dictionary

            # Check if the 'drinks' key is present in the response data
            if 'drinks' in data:
                # Return the list of drinks that contain the specified ingredient
                return data['drinks']
            else:
                # If no drinks were found, return an empty list
                st.warning(f"No cocktails found with ingredient: {ingredient}")
                return []
        else:
            # If the request was not successful, display an error message with the status code
            st.error(f"Error {response.status_code}: Failed to fetch data for ingredient '{ingredient}' from TheCocktailDB")
            return []

    # Handle network-related errors (timeout, DNS issues, etc.)
    except requests.exceptions.RequestException as e:
        # Display an error message in Streamlit with details about the exception
        st.error(f"Request exception: {e}")
        return []

# This function fetches detailed information for a specific cocktail based on its ID.
def fetch_cocktail_details(cocktail_id):
    # Construct the full API URL by appending the cocktail ID to the lookup URL
    api_url = f"{API_URL_LOOKUP}{cocktail_id}"

    try:
        # Send a GET request to the API URL to fetch detailed cocktail information
        response = requests.get(api_url, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response from the API
            data = response.json()  # create dictionary

            # Check if the 'drinks' key is present in the response data
            if 'drinks' in data:
                # Return the first cocktail in the 'drinks' list (since we're looking up by ID, it returns one drink)
                return data['drinks'][0]
            else:
                # If no drink was found, return None
                st.warning(f"No details found for cocktail ID: {cocktail_id}")
                return None
        else:
            # If the request was not successful, display an error message with the status code
            st.error(f"Error {response.status_code}: Failed to fetch cocktail details for ID '{cocktail_id}'")
            return None

    # Handle network-related errors (timeout, DNS issues, etc.)
    except requests.exceptions.RequestException as e:
        # Display an error message in the Streamlit app with details about the exception
        st.error(f"Request exception: {e}")
        return None
