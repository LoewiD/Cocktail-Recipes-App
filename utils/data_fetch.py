import requests
import streamlit as st

API_KEY = 'hqkablvRuIR0glAy0lCBTg==8bEjDHjU436g4F4M'  # API Key from API Ninjas (Dennis)

def fetch_cocktails_by_ingredients(ingredient):
    api_url = f"https://api.api-ninjas.com/v1/cocktail?name={ingredient}"
    headers = {
        'X-Api-Key': API_KEY
    }

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Parse JSON response
        else:
            st.error(f"Error {response.status_code}: Failed to fetch data from API Ninjas")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request exception: {e}")
        return None
