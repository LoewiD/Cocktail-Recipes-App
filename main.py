# main.py
import streamlit as st
from utils.user_interaction import get_user_input
from utils.data_fetch import fetch_cocktails_by_ingredient, fetch_cocktail_details
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib

# App Title
st.title("Cocktail Recipe Suggestion App")

# Load the training data to get the valid cocktail IDs and motif popularity scores
try:
    df_training_data = pd.read_csv("cocktails_data.csv")
    df_training_data['idDrink'] = df_training_data['idDrink'].astype(str).str.strip()  # Ensure IDs are treated as strings and strip whitespace
    valid_cocktail_ids = set(df_training_data["idDrink"])  # Use normalized IDs
    st.write(f"Loaded training data with {len(valid_cocktail_ids)} valid cocktail IDs.")
except FileNotFoundError:
    st.error("The training data CSV file could not be found. Please ensure 'cocktails_data.csv' is available.")
    valid_cocktail_ids = set()

# Load the trained models
try:
    kmeans_model = joblib.load('kmeans_motif_clustering_model.pkl')
    random_forest_model = joblib.load('random_forest_Popularity_Default_model.pkl')
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError as e:
    st.error(f"Required model file not found: {e.filename}. Please ensure model training has been completed successfully.")
    kmeans_model, random_forest_model, scaler = None, None, None

# Get user inputs (from the user_interaction.py script)
ingredients, motif_selection, category, glass_type, alcoholic_content = get_user_input()

# Ensure the user selected at least one ingredient
if ingredients and valid_cocktail_ids and random_forest_model and scaler:
    st.write(f"You selected ingredients: {', '.join(ingredients)}")

    # Step 1: Fetch cocktails for the first ingredient and store their 'idDrink' values in a set for comparison
    cocktails_for_ingredient = fetch_cocktails_by_ingredient(ingredients[0])
    common_cocktails = set(str(cocktail['idDrink']).strip() for cocktail in cocktails_for_ingredient)  # Normalize IDs
    st.write(f"Fetched {len(common_cocktails)} cocktails for ingredient '{ingredients[0]}'.")

    # Step 2: Intersect the results with cocktails from the other ingredients
    for ingredient in ingredients[1:]:
        cocktails_for_ingredient = fetch_cocktails_by_ingredient(ingredient)
        ingredient_cocktails = set(str(cocktail['idDrink']).strip() for cocktail in cocktails_for_ingredient)  # Normalize IDs
        st.write(f"Fetched {len(ingredient_cocktails)} cocktails for ingredient '{ingredient}'.")
        # Keep only cocktails that are in both sets (intersection)
        common_cocktails.intersection_update(ingredient_cocktails)
        st.write(f"{len(common_cocktails)} cocktails remain after filtering for ingredient '{ingredient}'.")

    # Step 3: Filter cocktails that are not in the CSV training data (only by cocktail ID)
    valid_common_cocktails = common_cocktails.intersection(valid_cocktail_ids)
    st.write(f"{len(valid_common_cocktails)} cocktails remain after checking against training data.")

    # Step 4: Fetch details of the remaining valid common cocktails
    if valid_common_cocktails:
        detailed_cocktails = []

        # Fetch details of each common cocktail and collect it
        for cocktail_id in valid_common_cocktails:
            details = fetch_cocktail_details(cocktail_id)
            if details:
                detailed_cocktails.append(details)

        # Convert detailed cocktails to DataFrame to display
        if detailed_cocktails:
            df = pd.DataFrame(detailed_cocktails)

            # Step 5: Apply filtering for other user preferences (category, glass type, alcoholic content)
            if category != "Don't care":
                df = df[df['strCategory'].str.lower() == category.lower()]

            if glass_type != "Don't care":
                df = df[df['strGlass'].str.lower() == glass_type.lower()]

            if alcoholic_content != "Don't care":
                df = df[df['strAlcoholic'].str.lower() == alcoholic_content.lower()]

            # If no cocktails match the selected filters, stop here
            if df.empty:
                st.error("No cocktails match the selected category, glass type, or alcohol content.")
            else:
                # Step 6: Predict popularity for each cocktail and sort
                df_for_prediction = df_training_data[df_training_data['idDrink'].isin(df['idDrink'])]

                if not df_for_prediction.empty:
                    X = df_for_prediction[["Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic"]]
                    X_scaled = scaler.transform(X)

                    # Predict popularity and sort by predicted scores
                    df['Predicted_Popularity'] = random_forest_model.predict(X_scaled)
                    df = df.sort_values(by='Predicted_Popularity', ascending=False).head(10)

                    # Display recommendations
                    st.write("Here are some cocktail suggestions based on your preferences:")
                    for _, cocktail in df.iterrows():
                        st.subheader(cocktail.get('strDrink', 'Unknown Cocktail'))  # Name of the cocktail

                        # Check for the image link before displaying
                        if 'strDrinkThumb' in cocktail and pd.notna(cocktail['strDrinkThumb']):
                            st.image(cocktail['strDrinkThumb'])  # Display the image of the cocktail
                        else:
                            st.write("(No image available)")

                        st.write(f"Category: {cocktail.get('strCategory', 'Unknown')}")
                        st.write(f"Glass: {cocktail.get('strGlass', 'Unknown')}")
                        st.write(f"Alcoholic: {cocktail.get('strAlcoholic', 'Unknown')}")
                        st.write(f"Instructions: {cocktail.get('strInstructions', 'No instructions available')}")

                        # Display ingredients and measurements
                        ingredients_list = [
                            cocktail[f'strIngredient{i}']
                            for i in range(1, 16)
                            if pd.notna(cocktail.get(f'strIngredient{i}'))
                        ]
                        measurements = [
                            cocktail[f'strMeasure{i}']
                            for i in range(1, 16)
                            if pd.notna(cocktail.get(f'strMeasure{i}'))
                        ]

                        if ingredients_list:
                            st.write("Ingredients:")
                            for ingredient, measure in zip(ingredients_list, measurements):
                                st.write(f"{measure} {ingredient}")
                        else:
                            st.write("(No ingredients available)")
                else:
                    st.error("No matching data found for popularity prediction.")
else:
    st.warning("Please select at least one ingredient and make sure the training data and models are available.")
