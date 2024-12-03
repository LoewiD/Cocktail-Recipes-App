# 🍹 Cocktail Recipes App

## Overview
The **Cocktail Recipes App** is a tool for discovering, 
saving, and managing cocktail recipes. With features like 
ingredient-based search, random cocktail suggestions, and machine learning-powered 
difficulty prediction. It's a consumer use based program and a helpful gadget to plan a party.

## Features
- **My Cocktails**: Save your favorite cocktails and generate a PDF shopping list with detailed recipes.
- **Ingredient Statistics**: Visualize popular ingredients across cocktails.
- **Search by Ingredients**: Find cocktails based on the ingredients you have.
- **Search by Name**: Look up specific cocktails.
- **Feeling Lucky**: Get a random cocktail suggestion.
- **Difficulty Prediction**: Predict the difficutly of a cocktail based on ML predictions

## Requirements
- **Python 3.12**
- **Dependencies**:
  - `pandas`
  - `requests`
  - `fpdf`
  - `joblib`
  - `scikit-learn`
  - `plotly`

Install all dependencies with:
```bash
pip install -r requirements.txt
```
It is possible that a new user might have to train the model themselves:
make sure you have the correct version of sklearn 1.5.2
```bash
pip show scikit-learn

scikit-learn==1.5.2
```
to train the model:
```bash
cd ml

python train_difficulty_model.py
```

## Application Startup
To run the Application you need to input the following code in your terminal:
```bash
streamlit run Main.py
```
or run the web-based, published version via: 
https://cocktail-recipes.streamlit.app

## Structure:
```
cocktail-recipes-app/
├── ml/
│   ├── train_difficulty_model.py     # Script for training the ML model
│   ├── difficulty_model.pkl          # Pre-trained ML model for difficulty prediction
│
├── pages/
│   ├── 1_My_Cocktails.py             # Page for managing favorite cocktails
│   ├── 2_Ingredient_Statistics.py    # Page for visualizing ingredient statistics
│   ├── 3_Search_Cocktails_by_Ingredient.py # Page for searching cocktails by ingredients
│   ├── 4_Search_Cocktails_by_Name.py       # Page for searching cocktails by name
│   ├── 5_I'm_Feeling_Lucky.py            # Page for random cocktail suggestions
│   ├── 6_Cocktail_Difficulty_Prediction.py # Page for difficulty prediction
│
├── utils/
│   ├── data_fetch.py                 # Functions to interact with APIs
│   ├── pdf_generation.py             # Functions to generate a PDF for shopping lists and recipes
│   ├── user_interaction.py           # Handles user inputs (e.g., ingredient selection)
│
├── main.py                           # Entry point of the Streamlit app
│
├── requirements.txt                  # List of Python dependencies
│
├── README.md                         # Instructions for setting up and using the app

```
## Help
If you need assistance with the application you can contact us via email.

# Contributors

- Alicia
- Daniel
- Dennis
- Gabriel
- Joel





