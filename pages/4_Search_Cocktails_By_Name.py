import streamlit as st
from utils.data_fetch import fetch_cocktail_by_name

# Page Title
st.title("🔍 Look Up Cocktails by Name")

# Initialize session state for cocktails if not already present
if "current_cocktails" not in st.session_state:
    st.session_state["current_cocktails"] = []  # Store fetched cocktails
if "my_cocktails" not in st.session_state:
    st.session_state["my_cocktails"] = []  # Store favorite cocktails

# User Input
cocktail_name = st.text_input("Enter the name of a cocktail:")

# Search Button
if st.button("Search"):
    if cocktail_name.strip():
        # Fetch cocktail data
        cocktails = fetch_cocktail_by_name(cocktail_name)
        if cocktails:
            st.session_state["current_cocktails"] = cocktails  # Save results in session state
        else:
            st.warning(f"No cocktails found for '{cocktail_name}'.")
    else:
        st.warning("Please enter a cocktail name to search.")

# Display Results from Session State
if st.session_state["current_cocktails"]:
    st.write(f"Results for **{cocktail_name}**:")
    for cocktail in st.session_state["current_cocktails"]:
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

        # Add to Favorites Button
        if st.button(f"Add {cocktail['strDrink']} to Favorites", key=f"add_{cocktail['idDrink']}"):
            if cocktail not in st.session_state["my_cocktails"]:
                st.session_state["my_cocktails"].append(cocktail)
                st.success(f"{cocktail['strDrink']} added to Favorites!")
            else:
                st.warning(f"{cocktail['strDrink']} is already in Favorites!")
