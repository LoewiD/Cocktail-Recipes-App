import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredients

# App Title
st.title("Cocktail Recipe Suggestion App")

# Get user inputs (from the external user_interaction.py file)
ingredients, taste_preference, glass_type, difficulty_level = get_user_input()

# Ensure the user selected at least one ingredient
if ingredients:
    st.write(f"You selected: {', '.join(ingredients)}") # joins the elements of the ingredients list into a single string, separating by a comma and a space.

    # Fetch cocktail suggestions for each selected ingredient
    all_cocktail_data = [] # empty list to store all the cocktail data fetched from the API for each ingredient
    for ingredient in ingredients: # Loops through each ingredient selected by the user from the ingredients list.
        cocktail_data = fetch_cocktails_by_ingredients(ingredient) # Calls the fetch_cocktails_by_ingredients(ingredient) function for each ingredient, which fetches the cocktail data from the API.
        if cocktail_data: # checks if it worked (not empty)
            all_cocktail_data.extend(cocktail_data) # extend() is used here to append multiple items from cocktail_data into all_cocktail_data (instead of adding the list as a single item).

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
