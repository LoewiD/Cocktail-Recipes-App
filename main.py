import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredient, fetch_cocktail_details

# App Title
st.title("Cocktail Recipe Suggestion App")

# Get user inputs (from the user_interaction.py script)
ingredients, taste_preference, glass_type, difficulty_level = get_user_input()

# Ensure the user selected at least one ingredient
if ingredients:
    st.write(f"You selected: {', '.join(ingredients)}") # join the elements of the ingredients list to a single string

    # Step 1: Fetch cocktails for the first ingredient and store their 'idDrink' values in a set for comparison
    common_cocktails = set(cocktail['idDrink'] for cocktail in fetch_cocktails_by_ingredient(ingredients[0]))

    # Step 2: Intersect the results with cocktails from the other ingredients (basically the same as above for the rest of the ingredients)
    for ingredient in ingredients[1:]: # start from index one and go all the way to the end of the list (for loop)
        cocktails_for_ingredient = fetch_cocktails_by_ingredient(ingredient)
        # Keep only cocktails that are in both sets (intersection)
        common_cocktails.intersection_update(cocktail['idDrink'] for cocktail in cocktails_for_ingredient)
        # modifies the common_cocktails set to keep only the elements that are present in both the original set and the cocktails_for_ingredient set

    # Step 3: Fetch details of the remaining common cocktails
    if common_cocktails:
        st.write("Here are some cocktail suggestions based on your ingredients:")
        for cocktail_id in common_cocktails:
            # Fetch detailed info for each cocktail
            details = fetch_cocktail_details(cocktail_id)
            if details:
                st.subheader(details['strDrink'])  # Name of the cocktail
                st.image(details['strDrinkThumb'])  # Display the image of the cocktail
                st.write(f"Category: {details['strCategory']}")  # Category
                st.write(f"Glass: {details['strGlass']}")  # Glass type
                st.write(f"Alcoholic: {details['strAlcoholic']}")  # Alcoholic or not
                st.write(f"Instructions: {details['strInstructions']}")  # Instructions

                # Display ingredients and measurements
                # Extract the ingredients and their corresponding measurements from the cocktail details,
                # looping through possible ingredient/measure fields (strIngredient1 to strIngredient15) and
                # only including those that are not empty.
                ingredients_list = [details[f'strIngredient{i}'] for i in range(1, 16) if details[f'strIngredient{i}']]
                measurements = [details[f'strMeasure{i}'] for i in range(1, 16) if details[f'strMeasure{i}']]

                st.write("Ingredients:")
                # The zip() function in Python is used to pair elements from two or more lists together,
                # creating tuples where each tuple contains one element from each list.
                # It works by combining corresponding elements from the lists into pairs.
                for ingredient, measure in zip(ingredients_list, measurements):
                    st.write(f"{measure} {ingredient}")
    else:
        st.error("No cocktails found with the selected ingredients.") # error message
else:
    st.warning("Please select at least one ingredient.") # error message if the user has not input any ingredients




