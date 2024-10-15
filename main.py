import streamlit as st
from utils.user_interaction import get_user_input


# App Title
st.title("Cocktail Recipe Suggestion App")

# Get user inputs (from the external user_interaction.py file)
ingredients, taste_preference, glass_type, difficulty_level = get_user_input()

# Show the ingredients the user entered
if ingredients:
    st.write(f"You have: {ingredients}")




