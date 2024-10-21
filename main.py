import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredients

# Title
st.title("Cocktail Recipe Suggestion App")

# Get user inputs (from the external user_interaction.py file)
ingredients, taste_preference, glass_type, difficulty_level = get_user_input()

# Show the ingredients the user entered
if ingredients:
    st.write(f"You have: {ingredients}")

    # Fetch cocktail suggestions based on ingredients
    cocktail_data = fetch_cocktails_by_ingredients(ingredients)

    # Ensure data is correctly fetched and contains the necessary details
    if cocktail_data:
        st.write("Here are some cocktail suggestions based on your ingredients:")

        for cocktail in cocktail_data:
            st.subheader(cocktail['name'])  # Cocktail name
            if 'instructions' in cocktail:
                st.write(cocktail['instructions'])  # Instructions on how to make the drink
            if 'ingredients' in cocktail:
                st.write(f"Ingredients: {', '.join(cocktail['ingredients'])}")


def cocktail_matches_taste(cocktail, taste_preference):
    # Placeholder function: Add logic to match the cocktail's taste profile
    # For example, you could compare the taste preferences stored in the cocktail data
    return True


def cocktail_matches_difficulty(cocktail, difficulty_level):
    # Placeholder function: Add logic to determine difficulty level match
    # For example, use predefined difficulty ratings for each cocktail
    return True




