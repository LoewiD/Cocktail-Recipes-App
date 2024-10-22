import streamlit as st
from utils.data_fetch import fetch_all_ingredients

def get_user_input():
    # Fetch all available ingredients from the API
    ingredient_options = fetch_all_ingredients()

    if ingredient_options:
        # User selects ingredients using multiselect
        ingredients = st.multiselect("Select ingredients you have:", ingredient_options)

        # User selects taste preference (with a "Don't Care" option)
        taste_preference = st.selectbox("Choose your taste preference:",
                                        ["Don't care", 'Sweet', 'Sour', 'Bitter', 'Fruity'])

        # User selects glass type (with a "Don't Care" option)
        glass_type = st.selectbox("Choose glass type:", ["Don't care", 'Highball', 'Martini', 'Coupe', 'Shot'])

        # User selects difficulty level (with a "Don't Care" option)
        difficulty_level = st.selectbox("Select difficulty level:", ["Don't care", 'Easy', 'Intermediate', 'Hard'])

        return ingredients, taste_preference, glass_type, difficulty_level
    else:
        st.error("No ingredients available to select.")
        return [], "Don't care", "Don't care", "Don't care"
