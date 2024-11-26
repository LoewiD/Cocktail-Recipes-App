import requests
import streamlit as st

# API URLs used for fetching ingredients, cocktails based on ingredients, and detailed cocktail information.
API_URL_INGREDIENTS = "https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"  # Endpoint to fetch all available ingredients
API_URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="  # Endpoint to fetch cocktails based on an ingredient
API_URL_LOOKUP = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i="  # Endpoint to fetch detailed cocktail info based on cocktail ID


# This function fetches all available ingredients from TheCocktailDB API. We use is for the Multiselect in user_interaction
@st.cache_data # caching data in order to not overload the api
def fetch_all_ingredients():
    try:
        response = requests.get(API_URL_INGREDIENTS)
        if response.status_code == 429:
            st.error("Rate limit exceeded. Please try again later.")
            return []
        elif response.status_code == 200:
            data = response.json()
            if 'drinks' in data:
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


# This function fetches cocktails from TheCocktailDB API for a single ingredient.
def fetch_cocktails_by_ingredient(ingredient):  # ingredient as a placeholder for the chosen ingredient in the multiselect

    # Construct the full API URL by appending the ingredient to the base URL
    api_url = f"{API_URL_BASE}{ingredient}"

    try:
        # Send a GET request to the API URL to fetch cocktails containing the specified ingredient
        response = requests.get(api_url)

        # Check if the request was successful (HTTP status code 200 means OK/good)
        if response.status_code == 200:
            # Parse (analyse) the JSON response from the API
            data = response.json()  # The API response is a JSON object --> converted into python dictionary

            # Check if the 'drinks' key is present in the response data
            if 'drinks' in data:
                # Return the list of drinks that contain the specified ingredient
                return data['drinks']
            else:
                # If no drinks were found, return an empty list
                return []
        else:
            # If the request was not successful, display an error message with the status code
            st.error(f"Error {response.status_code}: Failed to fetch data from TheCocktailDB")
            return []

    # Handle network-related errors
    except requests.exceptions.RequestException as e:
        # Display an error message
        st.error(f"Request exception: {e}")
        return []


# This function fetches detailed information for a specific cocktail based on its ID.
def fetch_cocktail_details(cocktail_id):

    # Construct the full API URL by appending the cocktail ID to the lookup URL
    api_url = f"{API_URL_LOOKUP}{cocktail_id}"

    try:
        # Send a GET request to the API URL to fetch detailed cocktail information
        response = requests.get(api_url)

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
                return None
        else:
            # If the request was not successful, display an error message with the status code
            st.error(f"Error {response.status_code}: Failed to fetch cocktail details")
            return None

    # Handle network-related errors
    except requests.exceptions.RequestException as e:
        # Display an error message in the Streamlit app
        st.error(f"Request exception: {e}")
        return None

def fetch_cocktail_by_name(name): #fetch cocktails by name

    api_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get("drinks", None)  # Return the 'drinks' list
        else:
            st.error(f"Error {response.status_code}: Failed to fetch data from TheCocktailDB")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request exception: {e}")
        return None

def fetch_random_cocktail():

    api_url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get("drinks", [None])[0]  # Return the first (and only) cocktail
        else:
            st.error(f"Error {response.status_code}: Failed to fetch data from TheCocktailDB")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request exception: {e}")
        return None
