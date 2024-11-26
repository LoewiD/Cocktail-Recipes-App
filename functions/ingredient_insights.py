import streamlit as st
from utils.data_fetch import fetch_all_ingredients, fetch_cocktails_by_ingredient


def ingredient_insights():
    st.header("Ingredient Usage Insights")

    # Fetch all ingredients and their cocktail counts
    ingredient_options = fetch_all_ingredients()
    if ingredient_options:
        usage_counts = {}
        for ingredient in ingredient_options:
            cocktails = fetch_cocktails_by_ingredient(ingredient)
            usage_counts[ingredient] = len(cocktails) if cocktails else 0

        # Plot ingredient usage
        st.subheader("Ingredient Popularity")
        st.bar_chart(usage_counts)
    else:
        st.error("Could not fetch ingredient data.")
