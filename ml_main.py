# ml_main.py

from ml_data_processing import load_and_process_data
from model_training import train_kmeans, train_random_forest
import joblib

# Step 1: Load and process data from CSV file
print("Step 1: Loading and processing data from CSV file...")
df, scaler = load_and_process_data(filename="cocktails_data.csv")
print("Data loading and processing completed.")

# Save scaler for later use in recommendations
joblib.dump(scaler, 'scaler.pkl')
print("Scaler has been saved.")

# Step 2: Train K-Means clustering model
print("Step 2: Training K-Means clustering model...")
df, kmeans = train_kmeans(df)
joblib.dump(kmeans, "kmeans_motif_clustering_model.pkl")
print("K-Means model has been saved.")

# Step 3: Train Random Forest models for popularity prediction
popularity_columns = ["Popularity_Default", "Popularity_Casual", "Popularity_Formal", "Popularity_Party", "Popularity_Romantic"]

for column in popularity_columns:
    print(f"Step 3: Training Random Forest model for {column} prediction...")
    model_filename = f"random_forest_{column}_model.pkl"
    rf_model = train_random_forest(df, target_column=column, model_filename=model_filename)
    print(f"Random Forest model for {column} has been saved.")

print("All models have been trained and saved successfully.")
