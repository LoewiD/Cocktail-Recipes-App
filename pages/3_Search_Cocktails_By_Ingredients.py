import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredient, fetch_cocktail_details

# Page Title
st.title("Search Cocktails by Ingredients")

# User selects ingredients
ingredients = get_user_input()

if ingredients:
    st.write(f"You selected: {', '.join(ingredients)}")

    # Fetch cocktails for the selected ingredients
    common_cocktails = set(cocktail['idDrink'] for cocktail in fetch_cocktails_by_ingredient(ingredients[0]))
    for ingredient in ingredients[1:]:
        cocktails_for_ingredient = fetch_cocktails_by_ingredient(ingredient)
        common_cocktails.intersection_update(cocktail['idDrink'] for cocktail in cocktails_for_ingredient)

    if common_cocktails:
        st.write("Here are some cocktail suggestions based on your ingredients:")
        for cocktail_id in common_cocktails:
            details = fetch_cocktail_details(cocktail_id)
            if details:
                # Display cocktail details
                st.subheader(details['strDrink'])
                st.image(details['strDrinkThumb'])
                st.write(f"Category: {details['strCategory']}")
                st.write(f"Glass: {details['strGlass']}")
                st.write(f"Alcoholic: {details['strAlcoholic']}")
                st.write(f"Instructions: {details['strInstructions']}")

                # Display ingredients and measurements
                ingredients_list = [details[f'strIngredient{i}'] for i in range(1, 16) if details[f'strIngredient{i}']]
                measurements = [details[f'strMeasure{i}'] for i in range(1, 16) if details[f'strMeasure{i}']]

                st.write("Ingredients:")
                for ingredient, measure in zip(ingredients_list, measurements):
                    st.write(f"{measure} {ingredient}")

                # Add Save Button
                if st.button(f"Save {details['strDrink']} to My Cocktails", key=f"save_{details['idDrink']}"):
                    # Initialize session state if not already done
                    if "my_cocktails" not in st.session_state:
                        st.session_state["my_cocktails"] = []

                    # Add cocktail to saved list if not already present
                    if details not in st.session_state["my_cocktails"]:
                        st.session_state["my_cocktails"].append(details)
                        st.success(f"{details['strDrink']} added to My Cocktails!")
                    else:
                        st.warning(f"{details['strDrink']} is already in My Cocktails!")
    else:
        st.error("No cocktails found with the selected ingredients.")
else:
    st.warning("Please select at least one ingredient.")
