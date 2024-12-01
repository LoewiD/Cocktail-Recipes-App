import streamlit as st # import streamlit to use streamlit functions
from utils.data_fetch import fetch_all_ingredients # we need the function from data_fetch.py

def get_user_input(): # definde function to get user input
    # Fetch all available ingredients from the API and store it in the options list
    ingredient_options = fetch_all_ingredients()

    if ingredient_options: # check if the options are there
        # User selects ingredients using multiselect (less room for errors by misspelling etc)
        ingredients = st.multiselect("Select ingredients:", ingredient_options)

        return ingredients
    else:
        st.error("No ingredients available to select.") # ensure that we have a return even if there is an error while fetching the data
        return [], "Don't care", "Don't care", "Don't care" # if we have an error we return an empty list and 3x don't care

