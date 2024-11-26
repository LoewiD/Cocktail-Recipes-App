import streamlit as st

def about():
    st.header("About the Cocktail Recipe App")
    st.write("""
        This app allows you to:
        - Search for cocktails by the ingredients you have on hand.
        - Explore ingredient usage trends in cocktails.
        - Save your favorite cocktails for future reference.
        - Learn more about cocktail preparation, difficulty, and glass types.
    """)
