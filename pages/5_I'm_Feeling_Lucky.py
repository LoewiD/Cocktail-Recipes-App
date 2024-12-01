import streamlit as st # we need streamlit functions
from utils.data_fetch import fetch_random_cocktail  # we need the random cocktails function which we defined in data_fetch.py

# Page Title
st.title("🍀 Random Cocktail Suggestion")
st.markdown("""
  Not sure what you want to drink?
    \n No problem! We have got you covered. Simply click on the button and get ready for a surprise!
   """)

# Initialize session state for random cocktail and favorites
if "current_random_cocktail" not in st.session_state:
    st.session_state["current_random_cocktail"] = None  # Store the current random cocktail
if "my_cocktails" not in st.session_state:
    st.session_state["my_cocktails"] = []  # Store favorite cocktails

# Button to Fetch a Random Cocktail
if st.button("Get a Random Cocktail"):
    # Fetch a random cocktail and store it in session state
    cocktail = fetch_random_cocktail() # here we use the function defined in the utils
    if cocktail:
        st.session_state["current_random_cocktail"] = cocktail # store it
    else:
        st.error("Failed to fetch a random cocktail. Please try again.") # error message if there was no cocktail found

# Display the Random Cocktail from Session State
if st.session_state["current_random_cocktail"]: # check if there is a cocktail in the current session state
    cocktail = st.session_state["current_random_cocktail"]
    st.subheader(cocktail["strDrink"]) # drink name
    st.image(cocktail["strDrinkThumb"], width=300) # drink picture
    st.write(f"**Category**: {cocktail['strCategory']}") # drink category
    st.write(f"**Glass**: {cocktail['strGlass']}") # drink glass type
    st.write(f"**Alcoholic**: {cocktail['strAlcoholic']}") # alcoholic vs non-alcoholic
    st.write(f"**Instructions**: {cocktail['strInstructions']}") # instructions for the drink

    # List ingredients and measurements
    st.write("**Ingredients**:")
    for i in range(1, 16): # loop through each of the 15 possible ingredients and measurements
        ingredient = cocktail.get(f"strIngredient{i}")
        measurement = cocktail.get(f"strMeasure{i}")
        if ingredient: # check for ingredients
            st.write(f"- {measurement or ''} {ingredient}") # display ingredients and measurements

    # Add to Favorites Button (session state "my_cocktails")
    if st.button(f"Save {cocktail['strDrink']} to Favorites", key=f"save_{cocktail['idDrink']}"):
        if cocktail not in st.session_state["my_cocktails"]: # checkt that the cocktail is not already in the session state!
            st.session_state["my_cocktails"].append(cocktail) # if that is not the case, we can add it
            st.success(f"{cocktail['strDrink']} added to Favorites!") # success message
        else:
            st.warning(f"{cocktail['strDrink']} is already in Favorites!") # error if the cocktail was already in the favorites
