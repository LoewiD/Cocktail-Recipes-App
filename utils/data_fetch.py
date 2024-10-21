import requests
import streamlit as st

API_KEY = 'hqkablvRuIR0glAy0lCBTg==8bEjDHjU436g4F4M'  # API Key for API Ninjas (Dennis)


def fetch_cocktails_by_ingredients(ingredient):
    api_url = f"https://api.api-ninjas.com/v1/cocktail?name={ingredient}"
    headers = {
        'X-Api-Key': API_KEY
    }

    try:  # try block handles the API request and any exceptions (errors)
        # for example if the network goes down or smth else it will jump
        # to the except block to handle the error without crashing the programm
        response = requests.get(api_url, headers=headers)       # requests.get(): This is a function from the
                                                                # requests library that performs the actual HTTP
                                                                #  GET request to fetch data from the API.
        if response.status_code == 200: # code 200 is good, the request has worked
            return response.json()  # Parse (analysieren) JSON response and returns a dictionairy or list
        else:
            st.error(f"Error {response.status_code}: Failed to fetch data from API Ninjas")
            return None # if request was unsucessful, an error message is displayed
    except requests.exceptions.RequestException as e:
        st.error(f"Request exception: {e}")
        return None
        # except block catches any errors (invalid URL, Network Problems,
        # timeouts, etc and stores the error message in "e" so that we could log it