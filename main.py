import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredient

# App Title
st.title("Cocktail Recipe Suggestion App")

# Get user inputs (from the external user_interaction.py file)
ingredients, taste_preference, glass_type, difficulty_level = get_user_input()

# Ensure the user selected at least one ingredient
if ingredients:
    st.write(f"You selected: {', '.join(ingredients)}")

    # Step 1: Fetch cocktails for the first ingredient
    common_cocktails = set(cocktail['idDrink'] for cocktail in fetch_cocktails_by_ingredient(ingredients[0]))

    # Step 2: Intersect the results with cocktails from the other ingredients
    for ingredient in ingredients[1:]:
        cocktails_for_ingredient = fetch_cocktails_by_ingredient(ingredient)
        # Keep only cocktails that are in both sets (intersection)
        common_cocktails.intersection_update(cocktail['idDrink'] for cocktail in cocktails_for_ingredient)

    # Step 3: Fetch details of the remaining common cocktails
    if common_cocktails:
        st.write("Here are some cocktail suggestions based on your ingredients:")
        for cocktail_id in common_cocktails:
            # Fetch detailed info for each cocktail (optional, not necessary with the 'filter.php' API)
            cocktail = next(cocktail for cocktail in fetch_cocktails_by_ingredient(ingredients[0]) if cocktail['idDrink'] == cocktail_id)
            st.subheader(cocktail['strDrink'])  # Name of the cocktail
            st.image(cocktail['strDrinkThumb'])  # Display the image of the cocktail
    else:
        st.error("No cocktails found with the selected ingredients.")
else:
    st.warning("Please select at least one ingredient.")
