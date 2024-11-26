import streamlit as st
from utils.data_fetch import fetch_cocktail_by_name

# Page Title
st.title("Look Up Cocktails by Name")

# User Input
cocktail_name = st.text_input("Enter the name of a cocktail:")

if st.button("Search"):
    if cocktail_name.strip():
        # Fetch cocktail data
        cocktails = fetch_cocktail_by_name(cocktail_name)

        if cocktails:
            st.write(f"Results for **{cocktail_name}**:")

            for cocktail in cocktails:
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
            st.warning(f"No cocktails found for '{cocktail_name}'.")
    else:
        st.warning("Please enter a cocktail name to search.")
