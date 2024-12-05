import streamlit as st # we need streamlit logic
from utils.user_interaction import get_user_input # we use the input from the user multiselect
from utils.data_fetch import fetch_cocktails_by_ingredient, fetch_cocktail_details # we utilize the functions defined in the data_fetch.py script

# Page Title
st.title("🍸 Search Cocktails by Ingredients")

st.markdown("""
  On this page you can search for cocktails using ingredients.
    \n Choose all the ingredients you want your cocktail to include and if there is a match, we'll make sure to present it to you.
   """)

# User selects ingredients
ingredients = get_user_input()

if ingredients:
    st.write(f"You selected: {', '.join(ingredients)}") # join the individual  choosen Ingredients (strings) into one single string (f formatting)

    # create an initial set of cocktails for the first ingredient
    # Use a set to ensure unique values and allow efficient intersection operations later
    common_cocktails = set(
        cocktail['idDrink'] for cocktail in fetch_cocktails_by_ingredient(ingredients[0])
    )

    # Loop through the remaining ingredients in the list (starting from the second one)
    for ingredient in ingredients[1:]:
        # Fetch the cocktails for the current ingredient
        cocktails_for_ingredient = fetch_cocktails_by_ingredient(ingredient)

        # Update the common_cocktails set by keeping only the cocktails present in both
        # the existing common_cocktails and the new set of cocktails fetched for this ingredient
        # This is done using the intersection_update method
        common_cocktails.intersection_update(
            cocktail['idDrink'] for cocktail in cocktails_for_ingredient
        )

    if common_cocktails: # check if there are any common cocktails
        st.write("Here are some cocktail suggestions based on your ingredients:")
        for cocktail_id in common_cocktails:
            details = fetch_cocktail_details(cocktail_id) # fetch the cocktail details using the cocktail_id (idDrink) and the search by id API
            if details: # check if Details have been found
                # Display cocktail details
                st.subheader(details['strDrink']) # Name of Drink
                st.image(details['strDrinkThumb']) # Picture of Drink
                st.write(f"**Category:** {details['strCategory']}") # Category of Drink
                st.write(f"**Glass:** {details['strGlass']}") # Glass Type of Drink
                st.write(f"**Alcoholic:** {details['strAlcoholic']}") # Alcoholic vs non-alcoholic
                st.write(f"**Instructions:** {details['strInstructions']}") # Instructions for the drink

                # Display ingredients and measurements
                ingredients_list = [details[f'strIngredient{i}'] for i in range(1, 16) if details[f'strIngredient{i}']] # check for ingredients 0-15 and add them to the ingredient list
                measurements = [details[f'strMeasure{i}'] for i in range(1, 16) if details[f'strMeasure{i}']] # check for measurements 0-15 and add them to the measurements list

                st.write("Ingredients:") # print Ingredients:
                for ingredient, measure in zip(ingredients_list, measurements): # use Zip to combine one ingredient to one measurement and create something like a dictionary
                    st.write(f"- {measure} {ingredient}") # display the zipped data

                # Add Save Button for the "My_Cocktails" Page
                if st.button(f"Save {details['strDrink']} to My Cocktails", key=f"save_{details['idDrink']}"): # saves the cocktail ID to the session state "my_cocktails"
                    # Initialize session state if not already done
                    if "my_cocktails" not in st.session_state:
                        st.session_state["my_cocktails"] = []

                    # Add cocktail to saved list if not already present
                    if details not in st.session_state["my_cocktails"]:
                        st.session_state["my_cocktails"].append(details)
                        st.success(f"{details['strDrink']} added to My Cocktails!") # success message
                    else:
                        st.warning(f"{details['strDrink']} is already in My Cocktails!") # warning message if we added the drink already
    else:
        st.error("No cocktails found with the selected ingredients.") # error message
else:
    st.warning("Please select at least one ingredient.") # error message
