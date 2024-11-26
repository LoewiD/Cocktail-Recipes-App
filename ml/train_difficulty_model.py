import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Step 1: Prepare Training Data
# Simulate cocktail data (in practice, fetch and preprocess from API or dataset)
data = pd.DataFrame({
    "Ingredients": [2, 4, 8, 3, 6, 5, 7],
    "Instruction_Length": [15, 30, 50, 20, 40, 35, 45],
    "Difficulty": ["Easy", "Medium", "Hard", "Easy", "Medium", "Medium", "Hard"]
})

# Encode Difficulty as numeric
data["Difficulty"] = data["Difficulty"].map({"Easy": 0, "Medium": 1, "Hard": 2})

# Step 2: Define Features and Labels
X = data[["Ingredients", "Instruction_Length"]]
y = data["Difficulty"]

# Step 3: Split Data for Training and Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Step 5: Save the Trained Model
joblib.dump(model, "ml/difficulty_model.pkl")
print("Model trained and saved as difficulty_model.pkl")
