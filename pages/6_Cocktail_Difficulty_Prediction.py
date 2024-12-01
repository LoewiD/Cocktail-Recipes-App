import streamlit as st
import joblib


# Load the trained model
model = joblib.load("ml/difficulty_model.pkl")

# Page Title
st.title("💡 Cocktail Difficulty Prediction")

# User Inputs
st.subheader("Enter Cocktail Features")
num_ingredients = st.number_input("Number of Ingredients", min_value=1, max_value=15, step=1)
instruction_length = st.number_input("Instruction Length (words)", min_value=5, max_value=500, step=5)

# Predict Difficulty
if st.button("Predict Difficulty"):
    prediction = model.predict([[num_ingredients, instruction_length]])
    difficulty_map = {0: "Easy", 1: "Medium", 2: "Hard"}
    st.write(f"Predicted Difficulty: **{difficulty_map[prediction[0]]}**")

# Optional: Show Tips
st.info("""
### Tips for Difficulty Levels:
- **Easy**: Minimal ingredients, short/simple instructions.
- **Medium**: Moderate ingredients and complexity.
- **Hard**: Many ingredients or detailed preparation steps.
""")
