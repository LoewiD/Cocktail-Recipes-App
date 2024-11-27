import streamlit as st
from utils.data_fetch import fetch_random_cocktail

# Page Title
st.title("🍀 Random Cocktail Suggestion")

# Initialize session state for random cocktail and favorites
if "current_random_cocktail" not in st.session_state:
    st.session_state["current_random_cocktail"] = None  # Store the current random cocktail
if "my_cocktails" not in st.session_state:
    st.session_state["my_cocktails"] = []  # Store favorite cocktails

# Button to Fetch a Random Cocktail
if st.button("Get a Random Cocktail"):
    # Fetch a random cocktail and store it in session state
    cocktail = fetch_random_cocktail()
    if cocktail:
        st.session_state["current_random_cocktail"] = cocktail
    else:
        st.error("Failed to fetch a random cocktail. Please try again.")

# Display the Random Cocktail from Session State
if st.session_state["current_random_cocktail"]:
    cocktail = st.session_state["current_random_cocktail"]
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
    if st.button(f"Save {cocktail['strDrink']} to Favorites", key=f"save_{cocktail['idDrink']}"):
        if cocktail not in st.session_state["my_cocktails"]:
            st.session_state["my_cocktails"].append(cocktail)
            st.success(f"{cocktail['strDrink']} added to Favorites!")
        else:
            st.warning(f"{cocktail['strDrink']} is already in Favorites!")
