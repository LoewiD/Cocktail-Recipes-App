import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from ml_data_processing import process_data, load_and_process_data
import pandas as pd

def train_kmeans(df, n_clusters=4):
    """
    Train a K-Means clustering model to group cocktails by motifs.
    
    Parameters:
        df (DataFrame): DataFrame containing cocktail data.
        n_clusters (int): Number of clusters for KMeans.

    Returns:
        DataFrame: Updated DataFrame with a new 'Motif_Cluster' column.
        KMeans: Trained KMeans model.
    """
    # Select motif columns for clustering
    motif_columns = ["Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic"]
    motif_data = df[motif_columns]

    # Initialize and fit KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Motif_Cluster'] = kmeans.fit_predict(motif_data)

    print("K-Means clustering completed.")
    print(f"Cluster Centers:\n{kmeans.cluster_centers_}")

    # Save the KMeans model
    joblib.dump(kmeans, "kmeans_motif_clustering_model.pkl")
    print("K-Means model has been saved.")

    # Save the updated DataFrame to ensure 'Motif_Cluster' is persisted
    df.to_csv("cocktails_data.csv", index=False, encoding='utf-8')
    print("Updated data with 'Motif_Cluster' saved to cocktails_data.csv")

    return df, kmeans

def train_random_forest(df):
    """
    Train a Random Forest Regressor to predict cocktail popularity.
    
    Parameters:
        df (DataFrame): DataFrame containing processed cocktail data.
    
    Returns:
        RandomForestRegressor: Trained Random Forest model.
        StandardScaler: Scaler used to normalize the data.
    """
    # Process the data to get train-test splits
    X_train, X_test, y_train, y_test, scaler = process_data(df)

    # Initialize and train the Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Evaluate model performance on the test set
    y_pred = rf_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("Random Forest Model Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"R^2 Score: {r2:.2f}")

    # Save the trained Random Forest model and scaler
    joblib.dump(rf_model, "random_forest_popularity_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    print("Random Forest model and scaler have been saved.")

    return rf_model, scaler

if __name__ == "__main__":
    # Load data and perform K-Means clustering
    df = pd.read_csv("cocktails_data.csv")
    df, kmeans_model = train_kmeans(df)

    # Train Random Forest model with the newly labeled data
    rf_model, scaler = train_random_forest(df)
