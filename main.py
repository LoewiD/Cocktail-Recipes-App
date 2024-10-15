# this is the main code for the project. The entire Program will be launched using this file.
# we use python interpreter 3.12

import streamlit as st


# Title and description
st.title("Cocktail Recipe Suggestion App")
st.write("Enter your ingredients, and we'll suggest cocktails!")

# User inputs (ingredient selection)
ingredients = st.text_input("Enter ingredients you have (comma-separated):")

# Placeholder for drink suggestions
if ingredients:
    st.write("Here are some cocktail suggestions based on your ingredients:")
    # Logic to suggest cocktails based on ingredients goes here

# Display cocktail cards
# st.image("cocktail_image_url")  # Example of showing cocktail images

# User selects preferences for taste
taste_preference = st.selectbox("Choose your taste preference:", ['Sweet', 'Sour', 'Bitter', 'Fruity'])

# User selects glass type
glass_type = st.selectbox("Choose glass type:", ['Highball', 'Martini', 'Coupe', 'Shot'])

# User selects difficulty
difficulty_level = st.slider("Select difficulty level:", 1, 5)

import requests

def fetch_cocktails_by_ingredients(ingredients):
    api_url = f"www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredients}"
    response = requests.get(api_url)
    return response.json()

# In app.py, use this function to get cocktail suggestions
if ingredients:
    cocktail_data = fetch_cocktails_by_ingredients(ingredients)
    st.write(cocktail_data)


