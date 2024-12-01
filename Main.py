import streamlit as st # import streamlit so that we can use streamlit integrated functions with st.

# Page Title
st.title("The Ultimate Cocktail Recipes App!")

# Introduction text
st.write(
    """
    Discover, save, and create your favorite cocktails! 
    This app lets you explore cocktail recipes, manage your favorites, generate shopping lists, and even predict the difficulty of making a cocktail.
    """
)


# Features Overview markdown is better for styled text (bold in this case)
st.markdown("## 🔎 Explore Features")

# Feature Descriptions intro
st.markdown(
    """
    ### 🌟 Features
    Use the **sidebar** to navigate through the app. Below are the features you can explore:
    """
)

# Create a feature list with dictionairies with title, description and a suitable image (from CocktailDB website)
features = [
    {
        "title": "🏠 Main Page",
        "description": "An overview of the app features and navigation tips.",
        "image": "https://www.thecocktaildb.com/images/media/drink/metwgh1606770327.jpg",
    },
    {
        "title": "📝 My Cocktails",
        "description": "Save your favorite cocktails, manage your list, and generate a PDF for shopping-list and recipes.",
        "image": "https://www.thecocktaildb.com/images/media/drink/vrwquq1478252802.jpg",
    },
    {
        "title": "📊 Ingredient Statistics",
        "description": "Look up an ingredient and see how often it is being used in the recipes. Visualize the most popular ingredients and their usage trends in cocktails.",
        "image": "https://www.thecocktaildb.com/images/media/drink/yrqppx1478962314.jpg",
    },
    {
        "title": "🍸 Search Cocktails By Ingredients",
        "description": "Find cocktails based on the ingredients you have on hand or search for cocktails by the ingredients you like most.",
        "image": "https://www.thecocktaildb.com/images/media/drink/xxyywq1454511117.jpg",
    },
    {
        "title": "🔍 Search Cocktails By Name",
        "description": "Search for your favorite cocktails by name and get detailed recipes.",
        "image": "https://www.thecocktaildb.com/images/media/drink/3qpv121504366699.jpg",
    },
    {
        "title": "🍀 I'm Feeling Lucky",
        "description": "Get a random cocktail suggestion and discover something new!",
        "image": "https://www.thecocktaildb.com/images/media/drink/5noda61589575158.jpg",
    },
    {
        "title": "💡 Cocktail Difficulty Prediction",
        "description": "Predict how challenging a cocktail is to make using ML.",
        "image": "https://www.thecocktaildb.com/images/media/drink/wmkbfj1606853905.jpg",
    },
]

# Display features in an organized layout
for feature in features: # loops through all the features in the list we created above
    st.markdown(f"### {feature['title']}") # displays the title of the feature as a markdown lv3 = boldness lvl
    col1, col2 = st.columns([1, 3]) # create two collums. col1 is 1 part wide, col2 is 3 parts wide
    with col1:
        st.image(feature["image"], width=100) # col1 show the image of the feature with width 100
    with col2:
        st.markdown(feature["description"]) # col2 display the description of the feature

# just a random message to get the people going (provocative lol)
st.markdown(
    """
    ---
    ## 🎉 Ready to Start Mixing?
    Use the **sidebar** to explore features and start adding amazing cocktails to your list. Cheers! 🥂
    """
)
