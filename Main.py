import streamlit as st

# Page Title
st.title("🍹 The Ultimate Cocktail App 🍹")

# Introduction Section
st.markdown(
    """
    Welcome to **The Ultimate Cocktail App**, your one-stop destination for discovering, creating, and learning about cocktails!
    Whether you're a seasoned mixologist or just getting started, our app has something for everyone. 
    Use the sidebar to explore the following features:
    """
)

# Features Overview
st.subheader("🔎 Explore Features")

# Organize features into visually distinct sections using columns
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        ### 📊 Ingredient Statistics
        - Discover the most popular ingredients across all cocktails.
        - See which ingredients are most commonly used and their distribution.
        """
    )
    st.image("https://www.thecocktaildb.com/images/media/drink/qxvtst1461867579.jpg", caption="Explore Ingredients", use_column_width=True)

    st.markdown(
        """
        ### 🍸 Search Cocktails by Ingredient
        - Select ingredients you have on hand to find matching cocktail recipes.
        - Filter results by taste, glass type, and difficulty.
        """
    )
    st.image("https://www.thecocktaildb.com/images/media/drink/5noda61589575158.jpg", caption="Find Recipes", use_column_width=True)

with col2:
    st.markdown(
        """
        ### 🔍 Search Cocktails by Name
        - Enter the name of a cocktail to find detailed recipes.
        - Perfect if you know what you're looking for.
        """
    )
    st.image("https://www.thecocktaildb.com/images/media/drink/uqxqsy1468876703.jpg", caption="Search by Name", use_column_width=True)

    st.markdown(
        """
        ### 🍀 Feeling Lucky?
        - Get a random cocktail suggestion for inspiration.
        - Discover new and exciting cocktails you might not have tried!
        """
    )
    st.image("https://www.thecocktaildb.com/images/media/drink/3k9qic1493068931.jpg", caption="Random Cocktails", use_column_width=True)

# Cocktail Difficulty Prediction Section
st.subheader("💡 Cocktail Difficulty Prediction")
st.markdown(
    """
    - Predict the difficulty of making a cocktail based on the number of ingredients and instruction complexity.
    - Tailor your experience to your skill level.
    """
)
st.image("https://www.thecocktaildb.com/images/media/drink/yutxtv1473344210.jpg", caption="Predict Difficulty", use_column_width=True)

# Closing Section
st.markdown(
    """
    ---
    ## Ready to Dive In?
    Use the **sidebar** to navigate between the features and start exploring!
    If you have any feedback, let us know—cheers! 🥂
    """
)
