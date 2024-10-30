#user_interaction.py
import streamlit as st
from utils.data_fetch import fetch_all_ingredients

def get_user_input():
    """
    Get user inputs including ingredients, motifs, taste preferences, glass type, and difficulty level.

    Returns:
        tuple: Contains user-selected ingredients, optional motif preference, category, glass type, and alcohol content.
    """
    # Fetch all available ingredients from the API and store it in the options list
    ingredient_options = fetch_all_ingredients()

    if ingredient_options:
        # User selects ingredients using multiselect (less room for errors by misspelling etc)
        ingredients = st.multiselect("Select ingredients you have:", ingredient_options)

        # User optionally selects a motif for sorting using a selectbox
        motif_selection = st.selectbox("Optionally select a motif:", ["Don't care", 'Casual', 'Formal', 'Party', 'Romantic'])

        # User selects other features like category, glass type, and alcohol content
        category = st.selectbox("Choose cocktail category:", ["Don't care", 'Ordinary Drink', 'Cocktail', 'Shot', 'Punch / Party Drink', 'Coffee / Tea', 'Other/Unknown'])
        glass_type = st.selectbox("Choose glass type:", ["Don't care", 'Highball glass', 'Cocktail glass', 'Martini glass', 'Old-fashioned glass', 'Collins glass', 'Wine Glass', 'Champagne flute', 'Shot glass', 'Coupe'])
        alcoholic_content = st.selectbox("Alcohol content:", ["Don't care", 'Alcoholic', 'Non alcoholic', 'Optional alcohol'])

        return ingredients, motif_selection, category, glass_type, alcoholic_content
    else:
        st.error("No ingredients available to select.")  # ensure that we have a return even if there is an error while fetching the data
        return [], "Don't care", "Don't care", "Don't care", "Don't care"  # default values for motifs and options if no ingredients available
