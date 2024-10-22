import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredients

# App Title
st.title("Cocktail Recipe Suggestion App")

# Get user inputs (from the external user_interaction.py file)
ingredients, taste_preference, glass_type, difficulty_level = get_user_input()

# Ensure the user selected at least one ingredient
if ingredients:
    st.write(f"You selected: {', '.join(ingredients)}") # joins the elements of the ingredients list into a single string, separating by a comma and a space.

    # Fetch cocktail suggestions for each selected ingredient
    all_cocktail_data = [] # empty list to store all the cocktail data fetched from the API for each ingredient
    for ingredient in ingredients: # Loops through each ingredient selected by the user from the ingredients list.
        cocktail_data = fetch_cocktails_by_ingredients(ingredient) # Calls the fetch_cocktails_by_ingredients(ingredient) function for each ingredient, which fetches the cocktail data from the API.
        if cocktail_data: # checks if it worked (not empty)
            all_cocktail_data.extend(cocktail_data) # extend() is used here to append multiple items from cocktail_data into all_cocktail_data (instead of adding the list as a single item).

    # Remove duplicates if needed
    seen = set() # Initializes an empty set to keep track of cocktail names that have already been added to unique_cocktails.
    unique_cocktails = [] # Initializes an empty list to store only the unique cocktails
    for cocktail in all_cocktail_data: # loops through each cocktail in the list
        if cocktail['name'] not in seen:  # checks if the cocktail has already been added to the seen list, if not:
            unique_cocktails.append(cocktail) # adds the cocktail to the unique list
            seen.add(cocktail['name']) # adds the cocktail to the seen set to mark it as "seen before"

    # Display suggestions
    if unique_cocktails:
        st.write("Here are some cocktail suggestions based on your ingredients:")
        for cocktail in unique_cocktails: # loops through all cocktails in the unique list
            st.subheader(cocktail['name']) # Title = name of the cocktail
            if 'instructions' in cocktail: # checks if the API has Instructions and if yes we print it
                st.write(cocktail['instructions'])
            if 'ingredients' in cocktail: # checks if the API has ingredients and if yes we print them
                st.write(f"Ingredients: {', '.join(cocktail['ingredients'])}")
    else:
        st.error("No cocktails found with the selected ingredients.") # error Message in case there are no matching cocktails
else:
    st.warning("Please select at least one ingredient.") # message if the user has not yet selected any ingredients

#testing
