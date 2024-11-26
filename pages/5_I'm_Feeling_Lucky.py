import streamlit as st
from utils.data_fetch import fetch_random_cocktail

# Page Title
st.title("Random Cocktail Suggestion")

if st.button("Get a Random Cocktail"):
    # Fetch a random cocktail
    cocktail = fetch_random_cocktail()

    if cocktail:
        st.subheader(cocktail["strDrink"])
        st.image(cocktail["strDrinkThumb"], width=300)
        st.write(f"**Category**: {cocktail['strCategory']}")
        st.write(f"**Glass**: {cocktail['strGlass']}")
        st.write(f"**Alcoholic**: {cocktail['strAlcoholic']}")
        st.write(f"**Instructions**: {cocktail['strInstructions']}")

        # List ingredients and measurements
        st.write("**Ingredients**:")
        for i in range(1, 16):
            ingredient = cocktail.get(f"strIngredient{i}")
            measurement = cocktail.get(f"strMeasure{i}")
            if ingredient:
                st.write(f"- {measurement or ''} {ingredient}")
    else:
        st.error("Failed to fetch a random cocktail. Please try again.")
