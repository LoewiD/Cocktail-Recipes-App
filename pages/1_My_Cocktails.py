import streamlit as st
from utils.data_fetch import calculate_cocktail_features
from utils.pdf_generation import generate_pdf
import joblib
import tempfile

# Load the ML model
model = joblib.load("ml/difficulty_model.pkl")

# Page Title
st.title("🍹 My Cocktails")

# Check if there are saved cocktails
if "my_cocktails" in st.session_state and st.session_state["my_cocktails"]:
    cocktails = st.session_state["my_cocktails"]

    # Display saved cocktails
    for cocktail in cocktails:
        st.subheader(cocktail["strDrink"])
        st.image(cocktail["strDrinkThumb"], width=300)

        # Calculate features
        num_ingredients, instruction_length = calculate_cocktail_features(cocktail)

        # Predict difficulty
        prediction = model.predict([[num_ingredients, instruction_length]])[0]
        difficulty = {0: "Easy", 1: "Medium", 2: "Hard"}[prediction]

        # Display cocktail details
        st.write(f"**Difficulty**: {difficulty}")
        st.write(f"**Number of Ingredients**: {num_ingredients}")
        st.write(f"**Instruction Length**: {instruction_length} words")
        st.write(f"**Instructions**: {cocktail['strInstructions']}")

        # Option to remove a cocktail
        if st.button(f"Remove {cocktail['strDrink']} from My Cocktails", key=f"remove_{cocktail['idDrink']}"):
            st.session_state["my_cocktails"].remove(cocktail)
            st.success(f"{cocktail['strDrink']} removed from My Cocktails!")

    # PDF Generation Section
    st.markdown("### Generate a PDF with your favorite cocktails:")
    if st.button("Generate PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            # Generate the PDF and save to a temporary file
            generate_pdf(cocktails, tmp_file.name)
            st.success("PDF generated successfully!")
            with open(tmp_file.name, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name="Cocktail_Shopping_List_and_Recipes.pdf",
                    mime="application/pdf",
                )
else:
    st.info("You haven't saved any cocktails yet.")