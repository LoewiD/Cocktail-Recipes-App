import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_fetch import fetch_all_ingredients, fetch_cocktails_by_ingredient

@st.cache_data
def get_top_ingredients(): # fetches the 10 most popular ingredients

    # Fetch all ingredients
    ingredient_options = fetch_all_ingredients()
    if not ingredient_options:
        return []

    # Count the number of cocktails for each ingredient
    ingredient_counts = []
    for ingredient in ingredient_options:
        cocktails = fetch_cocktails_by_ingredient(ingredient)
        ingredient_counts.append({"Ingredient": ingredient, "Count": len(cocktails) if cocktails else 0})

    # Sort ingredients by count and take the top 10
    sorted_ingredients = sorted(ingredient_counts, key=lambda x: x["Count"], reverse=True)[:10]
    return sorted_ingredients


def ingredient_insights(): # pie chart of how often a single ingredient is used

    st.header("Ingredient Usage Insights")

    # Fetch all available ingredients
    ingredient_options = fetch_all_ingredients()
    if not ingredient_options:
        st.error("Could not fetch ingredient data.")
        return

    # User selects a single ingredient from the dropdown
    selected_ingredient = st.selectbox("Select an ingredient to see its usage:", ingredient_options)

    if selected_ingredient:
        # Fetch cocktails for the selected ingredient
        cocktails_with_ingredient = fetch_cocktails_by_ingredient(selected_ingredient)
        count_with_ingredient = len(cocktails_with_ingredient)

        # Assuming TheCocktailDB has around 600 cocktails in total (you can fetch this dynamically if needed)
        total_cocktails = 600
        count_without_ingredient = total_cocktails - count_with_ingredient

        if count_with_ingredient > 0:
            # Display count
            st.write(f"The ingredient **{selected_ingredient}** is used in **{count_with_ingredient}** out of **{total_cocktails}** cocktails.")

            # Prepare data for pie chart
            data = {
                "Category": [f"Cocktails with {selected_ingredient}", f"Cocktails without {selected_ingredient}"],
                "Count": [count_with_ingredient, count_without_ingredient]
            }

            # Create a pie chart
            fig = px.pie(
                data,
                names="Category",
                values="Count",
                title=f"Proportion of Cocktails Using {selected_ingredient}",
                color_discrete_sequence=["#00802f", "#e1d7c3"]  # Blue and Orange
            )

            # Display the pie chart
            st.plotly_chart(fig, use_container_width=True)

        # Fetch and display the static bar chart for top 10 most used ingredients
        st.subheader("Top 10 Most Used Ingredients Across All Cocktails")
        top_ingredients = get_top_ingredients()

        if top_ingredients:
            # Prepare data for bar chart
            bar_data = pd.DataFrame(top_ingredients)

            # Create a bar chart
            fig_bar = px.bar(
                bar_data,
                x="Ingredient",
                y="Count",
                title="Top 10 Most Used Ingredients",
                labels={"Count": "Number of Cocktails", "Ingredient": "Ingredient"},
                text="Count"
            )
            # Change the color of all bars to HSG green
            fig_bar.update_traces(marker_color="#00802f")

            # Adjust bar chart appearance
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(
                xaxis_tickangle=45,
                xaxis_title=None,
                yaxis_title=None,
                showlegend=False
            )

            # Display the bar chart
            st.plotly_chart(fig_bar, use_container_width=True)

get_top_ingredients()
ingredient_insights()

