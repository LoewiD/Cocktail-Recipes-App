# Cocktail Recipes App
Group Project Repository for Cocktail Recipes Application

requirements:
- streamlit
  - pip install streamlit (terminal)
  - pip install requests (terminal)

Structure:

project_directory/
├── app.py                   # Main Streamlit app script
├── utils/
│   ├── user_interaction.py   # Handles user input and interaction
│   ├── data_fetch.py         # Handles API calls and data fetching
│   └── model.py              # Contains ML model or recommendation system
├── requirements.txt          # Dependencies for Streamlit and other libraries
└── README.md                 # Project documentation

Idea:

log in
starting page: what would you like to do?
  choose from: search by ingredient, search by name, look up data, feeling lucky, etc
  direct to page with function that the user clicked on
navigation bar on the right for other functions


use data visualisation to express how many cocktails include vodka

search for ingredient --> app only gives out name and ID
  search by name/ID --> app gives instructions

add LLM API?

