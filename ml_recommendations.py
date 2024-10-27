import joblib
import pandas as pd

def recommend_cocktails(motif_casual, motif_formal, motif_party, motif_romantic, top_n=5):
    """
    Recommend cocktails based on motif preferences using K-Means clustering.
    
    Parameters:
        motif_casual (int): User preference for casual motif (0-10).
        motif_formal (int): User preference for formal motif (0-10).
        motif_party (int): User preference for party motif (0-10).
        motif_romantic (int): User preference for romantic motif (0-10).
        top_n (int): Number of recommendations to return.

    Returns:
        DataFrame: DataFrame containing cocktail recommendations with name, category, glass type, instructions, and popularity.
    """
    # Load models and data
    try:
        df = pd.read_csv("cocktails_data.csv")
    except FileNotFoundError:
        raise FileNotFoundError("The dataset 'cocktails_data.csv' was not found. Please ensure the data fetching step was completed successfully.")

    # Ensure the required columns exist
    required_columns = ["Motif_Cluster", "strDrink", "strCategory", "strGlass", "strInstructions", "Popularity_Default"]
    for column in required_columns:
        if column not in df.columns:
            raise KeyError(f"Missing required column '{column}' in dataset. Please ensure the dataset is generated correctly.")
    
    # Load the trained K-Means clustering model and scaler
    try:
        kmeans = joblib.load('kmeans_motif_clustering_model.pkl')
        scaler = joblib.load('scaler.pkl')
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Required model file not found: {e.filename}. Please ensure model training has been completed successfully.")

    # Create a DataFrame for user preferences using the correct column names
    user_preferences = pd.DataFrame(
        [[motif_casual, motif_formal, motif_party, motif_romantic]],
        columns=["Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic"]
    )

    # Transform user preferences using the scaler
    user_preferences_scaled = scaler.transform(user_preferences)

    # Predict the cluster for user preferences
    cluster_label = kmeans.predict(user_preferences_scaled)[0]

    # Filter cocktails by the predicted cluster
    recommendations = df[df['Motif_Cluster'] == cluster_label]

    # Sort by popularity to ensure the best options are returned
    if recommendations.empty:
        return pd.DataFrame(columns=["strDrink", "strCategory", "strGlass", "strInstructions", "Popularity_Default"])
    
    recommendations = recommendations.sort_values(by='Popularity_Default', ascending=False).head(top_n)

    # Return the name, category, glass type, instructions, and popularity of recommended cocktails
    return recommendations[["strDrink", "strCategory", "strGlass", "strInstructions", "Popularity_Default"]]
