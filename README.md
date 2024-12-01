# 🍹 Cocktail Recipes App

## Overview
The **Cocktail Recipes App** is a tool for discovering, saving, and managing cocktail recipes. With features like ingredient-based search, random cocktail suggestions, and machine learning-powered difficulty prediction.

## Features
- **My Cocktails**: Save your favorite cocktails and generate a PDF shopping list with detailed recipes.
- **Ingredient Statistics**: Visualize popular ingredients across cocktails.
- **Search by Ingredients**: Find cocktails based on the ingredients you have.
- **Search by Name**: Look up specific cocktails.
- **Feeling Lucky**: Get a random cocktail suggestion.


## Requirements
- **Python 3.9+**
- **Dependencies**:
  - `streamlit`
  - `requests`
  - `fpdf`
  - `joblib`
  - `Pillow`

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
```bash
python train_difficulty_model.py
```
Structure:
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
│   ├── 5_Feeling_Lucky.py            # Page for random cocktail suggestions
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



