# ml_main.py

from ml_data_fetching import fetch_cocktails
from ml_data_processing import load_and_process_data, process_data
from model_training import train_kmeans, train_random_forest
from ml_recommendations import recommend_cocktails
import joblib

# Step 1: Fetch and save data
print("Step 1: Fetching cocktail data...")
fetch_cocktails()

# Step 2: Load and process data
print("Step 2: Loading and processing data...")
df, scaler = load_and_process_data()

# Save the scaler for later use in recommendations
joblib.dump(scaler, 'scaler.pkl')

# Step 3: Train K-Means clustering model
print("Step 3: Training K-Means clustering model...")
df, kmeans = train_kmeans(df)
joblib.dump(kmeans, "kmeans_motif_clustering_model.pkl")

# Step 4: Train Random Forest model for popularity prediction
print("Step 4: Training Random Forest model for popularity prediction...")
rf_model, scaler_rf = train_random_forest(df)

# Note: Scaler is saved during the training function
# Save the Random Forest model
joblib.dump(rf_model, "random_forest_popularity_model.pkl")

# Step 5: Make a sample recommendation using the trained models
print("Step 5: Generating sample recommendations...")
sample_recommendations = recommend_cocktails(motif_casual=8, motif_formal=2, motif_party=6, motif_romantic=4, top_n=5)
print(sample_recommendations)
