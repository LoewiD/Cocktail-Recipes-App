# ml_data_processing.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_process_data(filename="cocktails_data.csv"):
    """
    Load and preprocess the cocktail data.
    
    Parameters:
        filename (str): Path to the CSV file containing cocktail data.
    
    Returns:
        DataFrame: Preprocessed DataFrame containing cocktail data.
        StandardScaler: Scaler fitted on the features used for scaling.
    """
    # Load the CSV file
    df = pd.read_csv(filename)
    
    # Convert motifs and popularity columns to numeric, forcing errors to NaN
    for col in [
        "Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic", 
        "Popularity_Default", "Popularity_Casual", "Popularity_Formal", 
        "Popularity_Party", "Popularity_Romantic"
    ]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with NaN values in motif or popularity columns
    df = df.dropna(subset=[
        "Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic", 
        "Popularity_Default"
    ])

    # Select features and target variable
    X = df[["Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic"]]
    
    # Standardize the feature set
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    df[["Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic"]] = X_scaled

    return df, scaler

def process_data(df, target_column):
    """
    Splits the data into training and test sets, and scales the features.
    
    Parameters:
        df (DataFrame): DataFrame containing cocktail data with selected features.
        target_column (str): The target popularity column to be predicted.
    
    Returns:
        tuple: Scaled train and test sets (X_train, X_test, y_train, y_test), and the fitted StandardScaler.
    """
    # Select features and target variable
    features = ["Motif_Casual", "Motif_Formal", "Motif_Party", "Motif_Romantic"]
    
    X = df[features]
    y = df[target_column]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the feature data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler
