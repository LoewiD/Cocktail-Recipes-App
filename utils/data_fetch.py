import requests # import the requests package to interact with Web-based APIs
import streamlit as st # import streamlit functionalities

# API URLs used for fetching ingredients, cocktails based on ingredients, and detailed cocktail information.
API_URL_INGREDIENTS = "https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"  # Endpoint to fetch all available ingredients
API_URL_BASE = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="  # Endpoint to fetch cocktails based on an ingredient
API_URL_LOOKUP = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i="  # Endpoint to fetch detailed cocktail info based on cocktail ID


# This function fetches all available ingredients from TheCocktailDB API. We use is for the Multiselect in user_interaction
@st.cache_data # caching data in order to not overload the api (the function gets used 5 times in the app)
# decorator in Streamlit is used to cache data fetched or computed by a function.
# This improves performance by storing the results of a function so that the app doesn’t need to recompute or refetch the data every time the app reruns.
# It also helps to dodge 429 errors (too many requests)

def fetch_all_ingredients(): # function definition to get all the ingredients
    try:
        response = requests.get(API_URL_INGREDIENTS) # API call to the "ingredients API" store data into "response"
        if response.status_code == 429: # if we have too many reqests, print this error message --> we should calm down and try again later
            st.error("Rate limit exceeded. Please try again later.")
            return []
        elif response.status_code == 200: # if the response worked (http status code 200) we can continue with the program
            data = response.json() # the response is a json file and we convert it into a python dictionairy "data" for us to use further using python syntax
            if 'drinks' in data: # check if the "drinks" key is in the "data" dictionairy
                return [ingredient['strIngredient1'] for ingredient in data['drinks']] # if yes, it returns a list compiled of all the strIngredient1 of all the drinks in the data
            else:
                st.error("No ingredients found.")
                return [] # if no, return an empty list and display the error message
        else:
            st.error(f"Error {response.status_code}: Failed to fetch ingredients from TheCocktailDB") # if there is another error while getting the API data, this error message gets displayed
            return []
    except requests.exceptions.RequestException as e: # Catches any exception raised by the requests library (e.g., connection errors, timeouts, or invalid URLs) and stores the error messages as e.
        st.error(f"Request exception: {e}") # displays an error message in the streamlit app
        return [] # gracefully handling the error and returning an empty list to keep the program from crashing.


# This function fetches cocktails from TheCocktailDB API for a single ingredient.
def fetch_cocktails_by_ingredient(ingredient):  # ingredient as a placeholder for the chosen ingredient in the multiselect

    # Construct the full API URL by appending the ingredient to the base URL with f formatting
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
                # Return the list of drinks (which are dictionaries) that contain the specified ingredient
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

    api_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}" # new API to find Cocktails by searching for the names of the cocktail

    try:
        response = requests.get(api_url) # request logic .get = API call
        if response.status_code == 200: # if the http code = 200 the call was successful
            data = response.json() # take the json data from the api call and convert it into a python dictionary to use it further with python syntax
            return data.get("drinks", None)  # tries to return the value of the key "drinks" from the dictionary "data". If the key does not exist, the return value is "none" --> empty list
        else:
            st.error(f"Error {response.status_code}: Failed to fetch data from TheCocktailDB") # error message in case the API call was unsucessful
            return None # return nothing since no data was found
    except requests.exceptions.RequestException as e: # same thing as above, handle network related errors and handle them gracefully
        st.error(f"Request exception: {e}")
        return None

def fetch_random_cocktail(): # get a random cocktail

    api_url = "https://www.thecocktaildb.com/api/json/v1/1/random.php" # API to get a random cocktail

    try:
        response = requests.get(api_url) # API call
        if response.status_code == 200: # if successful (http = 200)
            data = response.json() # convert the json data into a python dictionary (parse the json data in correct terms)
            return data.get("drinks", [None])[0]  # Return the first (and only) cocktail since we only want one random cocktail
        # we use [None] as opposed to None to avoid errors since here we want to get the results in a list (even if it is empty) otherwise we could get
        # the error that None is non-iterable and since it is the standart value we would not be able to overrwite it

        else:
            st.error(f"Error {response.status_code}: Failed to fetch data from TheCocktailDB") # error message
            return None # return nothing since no data was found
    except requests.exceptions.RequestException as e: # same network related error-handling as above
        st.error(f"Request exception: {e}")
        return None

def calculate_cocktail_features(cocktail): # function to calculate the number of ingredients and the length of the instructions

    num_ingredients = sum(1 for i in range(1, 16) if cocktail.get(f"strIngredient{i}")) # counts the number of ingredients by adding 1 for every strIngredient 1-15 that is not empty or "None"
    instruction_length = len(cocktail["strInstructions"].split()) if cocktail.get("strInstructions") else 0
    # checks if the strInstructions is present in the Data and splits the
    # individual words by spacings. then it counts how many individual words there are using the "len" logic
    # if there is no strInstructions available the the instruction_length is set to 0
    return num_ingredients, instruction_length # returns the two value for future use

