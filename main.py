import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredients

# App Title
st.title("Cocktail Recipe Suggestion App")

# Get user inputs (from the external user_interaction.py file)
ingredients, taste_preference, glass_type, difficulty_level = get_user_input()

# Ensure the user selected at least one ingredient
if ingredients:
    st.write(f"You selected: {', '.join(ingredients)}")

    # Fetch cocktail suggestions for each selected ingredient
    all_cocktail_data = []
    for ingredient in ingredients:
        cocktail_data = fetch_cocktails_by_ingredients(ingredient)
        if cocktail_data:
            all_cocktail_data.extend(cocktail_data)

    # Remove duplicates if needed
    seen = set()
    unique_cocktails = []
    for cocktail in all_cocktail_data:
        if cocktail['name'] not in seen:
            unique_cocktails.append(cocktail)
            seen.add(cocktail['name'])

    # Display suggestions
    if unique_cocktails:
        st.write("Here are some cocktail suggestions based on your ingredients:")
        for cocktail in unique_cocktails:
            st.subheader(cocktail['name'])
            if 'instructions' in cocktail:
                st.write(cocktail['instructions'])
            if 'ingredients' in cocktail:
                st.write(f"Ingredients: {', '.join(cocktail['ingredients'])}")
    else:
        st.error("No cocktails found with the selected ingredients.")
else:
    st.warning("Please select at least one ingredient.")
