import streamlit as st

def get_user_input():
    # User enters the ingredients they have
    ingredients = st.text_input("Enter ingredients you have (comma-separated):")

    # User selects taste preference (with a "Don't Care" option)
    taste_preference = st.selectbox("Choose your taste preference:", ["Don't care", 'Sweet', 'Sour', 'Bitter', 'Fruity'])

    # User selects glass type (with a "Don't Care" option)
    glass_type = st.selectbox("Choose glass type:", ["Don't care", 'Highball', 'Martini', 'Coupe', 'Shot'])

    # User selects difficulty level (with a "Don't Care" option)
    difficulty_level = st.selectbox("Select difficulty level:", ["Don't care", 'Easy', 'Intermediate', 'Hard'])

    return ingredients, taste_preference, glass_type, difficulty_level
