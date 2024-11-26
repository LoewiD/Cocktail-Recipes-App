import streamlit as st
from functions.search_cocktails import search_cocktails
from functions.ingredient_insights import ingredient_insights
from functions.favorites import favorites
from functions.about import about
from functions.start_page import start_page

# App Title
st.title("The Cocktail App")

# Sidebar Dropdown Menu
menu = st.sidebar.selectbox(
    "Choose a feature",
    ["Start Page", "Search Cocktails by Ingredients", "Ingredient Usage Insights", "Favorite Cocktails", "About"]
)

# Navigation
if menu == "Start Page":
    start_page()
elif menu == "Search Cocktails by Ingredients":
    search_cocktails()
elif menu == "Ingredient Usage Insights":
    ingredient_insights()
elif menu == "Favorite Cocktails":
    favorites()
elif menu == "About":
    about()

