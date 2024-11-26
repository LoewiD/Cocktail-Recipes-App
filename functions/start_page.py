import streamlit as st


def start_page():
    st.title("Welcome to the Cocktail Recipe App!")
    st.write("""
        🍹 **Discover Cocktails**:
        - Find cocktail recipes based on the ingredients you have at hand.
        - Explore trends and ingredient usage insights.
        - Save your favorite cocktails for easy access.

        🎉 **Get Started**:
        - Use the sidebar menu to navigate through the app features.
        - Enjoy crafting your next favorite drink!
    """)
    st.image(
        "https://www.thecocktaildb.com/images/media/drink/5noda61589575158.jpg",
        caption="A refreshing Margarita!"
    )
