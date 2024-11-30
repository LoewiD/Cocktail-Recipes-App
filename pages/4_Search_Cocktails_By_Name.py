import streamlit as st # streamlit functions
from utils.data_fetch import fetch_cocktail_by_name # import function from data_fetch.py script

# Page Title
st.title("🔍 Look Up Cocktails by Name")

# Initialize session state for cocktails if not already present
if "current_cocktails" not in st.session_state:
    st.session_state["current_cocktails"] = []  # stores cocktails displayed when we search for cocktails by name
if "my_cocktails" not in st.session_state:
    st.session_state["my_cocktails"] = []  # stores cocktails we want to add to the favorites

# User Input by textbox
cocktail_name = st.text_input("Enter the name of a cocktail:")

# Search Button
if st.button("Search"):
    if cocktail_name.strip(): # checks if the textbox has something written into it and removed empty spaces
        # Fetch cocktail data
        cocktails = fetch_cocktail_by_name(cocktail_name) # fetch cocktails by using the user input as the cocktail_name
        if cocktails: # check for found cocktails
            st.session_state["current_cocktails"] = cocktails  # Save results in (current cocktails) session state
        else:
            st.warning(f"No cocktails found for '{cocktail_name}'.") # error if no cocktails have been found
    else:
        st.warning("Please enter a cocktail name to search.")  # call for action to input a name

# Display Results from Session State
if st.session_state["current_cocktails"]:
    st.write(f"Results for **{cocktail_name}**:") # bold text with **
    for cocktail in st.session_state["current_cocktails"]: # loop through each cocktail in the current_cocktails session state
        st.subheader(cocktail["strDrink"]) # drink name
        st.image(cocktail["strDrinkThumb"], width=300) # image of drink with width = 300 (cosmetic)
        st.write(f"**Category**: {cocktail['strCategory']}") # category of the drink
        st.write(f"**Glass**: {cocktail['strGlass']}") # glass type of the drink
        st.write(f"**Alcoholic**: {cocktail['strAlcoholic']}") # alcoholic vs non-alcoholic
        st.write(f"**Instructions**: {cocktail['strInstructions']}") # instructions for the drink

        # List ingredients and measurements. this is the same thing as the zip function in the page before but coded differently to show two different ways
        st.write("**Ingredients**:")
        for i in range(1, 16):
            ingredient = cocktail.get(f"strIngredient{i}")
            measurement = cocktail.get(f"strMeasure{i}")
            if ingredient:
                st.write(f"- {measurement or ''} {ingredient}")

        # Add to Favorites Button
        if st.button(f"Add {cocktail['strDrink']} to Favorites", key=f"add_{cocktail['idDrink']}"):
            if cocktail not in st.session_state["my_cocktails"]: # make sure that the cocktail is not yet added to the saved favorites
                st.session_state["my_cocktails"].append(cocktail) # if that is not the case, add it
                st.success(f"{cocktail['strDrink']} added to Favorites!") # success message
            else:
                st.warning(f"{cocktail['strDrink']} is already in Favorites!") # error message if the drink was already added
