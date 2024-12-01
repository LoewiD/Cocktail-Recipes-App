import streamlit as st
import plotly.express as px # import the Plotly Express library to create interactive charts in python
import pandas as pd # import the pandas library to create the static graph and data analysis
import time # we need this for the sleep logic, otherwise the app crashes
from utils.data_fetch import fetch_all_ingredients, fetch_cocktails_by_ingredient # get the needed functions which we defined in the data_fetch.py script

@st.cache_data # we cashe the data again in an effort to minimize the risk of overexhausting the API (I am not sure if it does anything for this function but frankly I am too scared to change it again)
def get_top_ingredients(): # function that fetches the 10 most popular ingredients in all of the cocktails

    # Fetch all ingredients
    ingredient_options = fetch_all_ingredients()
    if not ingredient_options: # if it did not work,
        return [] # import pandas as pd

    # Count the number of cocktails for each ingredient
    ingredient_counts = [] # start with an empty list
    for ingredient in ingredient_options: # loop through the ingredients in the ingredient_options (all of them)
        time.sleep(0.5) #stupid API cannot handle a lot of requests so we have to delay the individual requests with a timer (0.5 second). PLS DO NOT DELETE! THE PAGE WILL CRASH!
        cocktails = fetch_cocktails_by_ingredient(ingredient) # we re-use the fetch_cocktails_by_ingredient function to count all the possible cocktails
        ingredient_counts.append({"Ingredient": ingredient, "Count": len(cocktails) if cocktails else 0})
        # the list gets edited to include the dict. for the possible cocktails. at the end we have a list of many dictionaries (ingredient : count)
        # the key is the Ingredient and the value is the "count" of possible drinks using the "len" logic

    # Sort ingredient_counts by count and take the top :10 (0-9)
    sorted_ingredients = sorted(ingredient_counts, key=lambda x: x["Count"], reverse=True)[:10]
    # lambda x creates a temporary function where x is the input (count), making it useful for short, one-time operations like sorting. we could also use a self defined function but it would not look as good
    return sorted_ingredients


def ingredient_insights(): # function definition of the pie chart of how often a single ingredient is used

    st.title("📊 Ingredient Usage Insights") # title

    st.markdown("""
    Here you can find out how often your favorite ingredient is used throughout the recipes. Simply select the ingredient you want insights for and the graph will adjust automatically!
    \n You can also take a look at the static bar chart to see an overview of the ten most used ingredients.
    
    """)

    # Fetch all available ingredients
    ingredient_options = fetch_all_ingredients()
    if not ingredient_options:
        st.error("Could not fetch ingredient data.") # error message
        return

    # selection of one single ingredient by the user using selectbox (options = ingredient_options)
    selected_ingredient = st.selectbox("Select an ingredient to see its usage:", ingredient_options)

    if selected_ingredient:
        # Fetch cocktails for the selected ingredient
        cocktails_with_ingredient = fetch_cocktails_by_ingredient(selected_ingredient)
        count_with_ingredient = len(cocktails_with_ingredient) # use the "len" logic to count all the cocktails in the "count_with_ingredient_list)

        # Assuming TheCocktailDB has around 600 cocktails in total
        total_cocktails = 600
        count_without_ingredient = total_cocktails - count_with_ingredient # get the difference for the other part of the pie chart

        if count_with_ingredient > 0:
            # Display count
            st.write(f"The ingredient **{selected_ingredient}** is used in **{count_with_ingredient}** out of **{total_cocktails}** cocktails.") # how many cocktails of the 600 available ones use the selected ingredient?

            # Prepare data for pie chart
            data = { # create dictionary with two keys
                "Category": [f"Cocktails with {selected_ingredient}", f"Cocktails without {selected_ingredient}"], # list with two strings (cocktails with and without ingredient)
                "Count": [count_with_ingredient, count_without_ingredient] # list of two numbers
            }

            # Create a pie chart and store it in the fig variable. We use the plotly express logic we imported at the start
            fig = px.pie(
                data, # dict. containing two categories "Categories" and "Count"
                names="Category", #from data
                values="Count",  # from date
                title=f"Proportion of Cocktails Using {selected_ingredient}", # title
                color_discrete_sequence=["#00802f", "#e1d7c3"]  # Colors (HSG Colours)
            )

            # Display the pie chart with streamlit integration
            st.plotly_chart(fig, use_container_width=True) # automatically adjust the graph width to adjust to the streamlit layout

        # Fetch and display the static bar chart for top 10 most used ingredients
        st.subheader("Top 10 Most Used Ingredients Across All Cocktails") # title
        top_ingredients = get_top_ingredients() # call the function which we defined earlier

        if top_ingredients:
            # Prepare data for bar chart
            bar_data = pd.DataFrame(top_ingredients) # use pandas logic to prepare the data for the chart

            # Create the bar chart
            fig_bar = px.bar(
                bar_data, # data used
                x="Ingredient", # define the x axis as "Ingredients" from data
                y="Count", # define y axis as "Count" from data
                title="Top 10 Most Used Ingredients", # title
                labels={"Count": "Number of Cocktails", "Ingredient": "Ingredient"}, # renames the y axis to " Number of Cocktails" for better clarity. (X axis does not change)
                text="Count" # text label over the individual bars to indicate the exact number of cocktails
            )

            # Change the color of all bars to HSG green opposed to the standard colour
            fig_bar.update_traces(marker_color="#00802f")

            # Adjust bar chart appearance (only cosmetic changes)
            fig_bar.update_traces(textposition='outside') # moves the text labels outside the chart instead of in the bars
            fig_bar.update_layout(
                xaxis_tickangle=45, # rotates the x-axis names (ingredients) by 45 degrees to improve readability
                xaxis_title=None, # removes the default x axis title
                yaxis_title=None, # removes the default y axis title (both to make it cleaner)
                showlegend=False  # remove the chart legend because the chart already labels everything sufficiently
            )

            # Display the bar chart using streamlit integration
            st.plotly_chart(fig_bar, use_container_width=True) # make it fit into our streamlit grid

get_top_ingredients() # since we only defined both functions, we also have to let them run in this step
ingredient_insights()

