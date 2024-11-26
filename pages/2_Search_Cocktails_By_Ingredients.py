import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredient, fetch_cocktail_details


st.header("Search Cocktails by Ingredients")
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
                st.subheader(details['strDrink'])
                st.image(details['strDrinkThumb'])
                st.write(f"Category: {details['strCategory']}")
                st.write(f"Glass: {details['strGlass']}")
                st.write(f"Alcoholic: {details['strAlcoholic']}")
                st.write(f"Instructions: {details['strInstructions']}")

                ingredients_list = [details[f'strIngredient{i}'] for i in range(1, 16) if
                                    details[f'strIngredient{i}']]
                measurements = [details[f'strMeasure{i}'] for i in range(1, 16) if details[f'strMeasure{i}']]

                st.write("Ingredients:")
                for ingredient, measure in zip(ingredients_list, measurements):
                       st.write(f"{measure} {ingredient}")
    else:
        st.error("No cocktails found with the selected ingredients.")
else:
    st.warning("Please select at least one ingredient.")
