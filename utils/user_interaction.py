import streamlit as st

def get_user_input():
    # User enters the ingredients they have
    ingredients = st.text_input("Enter ingredients you have (comma-separated):")

    # User selects taste preference
    taste_preference = st.selectbox("Choose your taste preference:", ['Sweet', 'Sour', 'Bitter', 'Fruity'])

    # User selects glass type
    glass_type = st.selectbox("Choose glass type:", ['Highball', 'Martini', 'Coupe', 'Shot'])

    # User selects difficulty level
    difficulty_level = st.slider("Select difficulty level:", 1, 5)

    return ingredients, taste_preference, glass_type, difficulty_level
