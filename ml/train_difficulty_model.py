import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import joblib

# load the (previously generated) dataset
data = pd.read_csv("cocktails_data.csv")

# print columns for debugging
print("Columns in CSV:", data.columns)

# extract features from the CSV headers based on relevant information
# these features were provided in the CSV as additional complexity and measurement values
features = [
    "num_ingredients",
    "instruction_length",
    "num_measurements",
    "preparation_complexity",
    "ingredient_complexity",
    "instruction_complexity",
    "tool_complexity",
    "glass_type_complexity"
]

# define the features dataframe
X = data[features]

# generate difficulty level labels for training
# since there is not a predefined difficulty level, generate a pseudo-label using 'preparation_complexity' as a basis
# assigning difficulty levels manually for simplicity (for demonstration purposes, adjust if necessary)
y = pd.cut(
    data['preparation_complexity'] + data['instruction_complexity'],
    bins=[-1, 2, 5, float('inf')],  #adjust these values for better distribution (default while testing: -1, 4, 7), current values after XYZ-Analysis of data
    labels=['Easy', 'Moderate', 'Hard']
)

# split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)       #..._train used to train the model, ..._test used to test the model
# test_size=0.2 reserves 20% of the data for testing,

# train a Random Forest Classifier with Hyperparameter Tuning, adjust if necessary
param_grid = {
    'n_estimators': [100, 200, 300],            #number of trees in the forest, default while testing: 100, 200, 300
    'max_depth': [None, 10, 20],            #maximum depth of each tree, default while testing: None, 10, 20
    'min_samples_split': [2, 5, 10]         #minimum number of samples required to split an internal node, default while testing: 2, 5, 10
}

rf_model = RandomForestClassifier(random_state=42)      #controlls randomness (if bootstrapping=True) and sampling of features
grid_search = GridSearchCV(rf_model, param_grid, cv=3, scoring='accuracy', n_jobs=-1)       #performs hyperparameter tuning by trying different combinations of the values in param_grid, cv=3 means 3-fold cross-validation, parameter specifies how many CPU cores to use for training (-1 uses all cores)
grid_search.fit(X_train, y_train)       #trains the RandomForest model using different parameter combinations to find the one that provides the best accuracy

# best model from GridSearchCV
best_model = grid_search.best_estimator_

# evaluate the model
y_pred = best_model.predict(X_test)         #predicts the difficulty level for the samples in the test set
accuracy = accuracy_score(y_test, y_pred)           #calculates percentage of correct predictions
print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# save the trained model for later use
joblib.dump(best_model, "difficulty_model.pkl")
print("Model saved as difficulty_model.pkl")
