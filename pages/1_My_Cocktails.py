import streamlit as st # use streamlit
from utils.data_fetch import calculate_cocktail_features # we need the data_fetch script for the calculate_cocktail_features function
from utils.pdf_generation import generate_pdf # we need the pdf logic to create the pdf button
import joblib # Handles saving and loading Python objects efficiently. we need it to import our pre-trained ML model
import tempfile # Creates temporary files and directories that are automatically deleted when no longer needed.
                # we use it to create a temporary PDF for the user to download while not cluttering the file system

### Delete the lower two ### to check sklearn version if we have an error
### import sklearn
### st.write(sklearn.__version__)

# Load the pre-trained ML model using joblib (we have to have it trained Manually before!)
model = joblib.load("ml/difficulty_model.pkl")

# Page Title
st.title("🍹 My Cocktails")

# Check if there are saved cocktails. St.session_state is a special dictionary-like object in Streamlit used to persist data across app reruns.
if "my_cocktails" in st.session_state and st.session_state["my_cocktails"]: #checks that the key "my_cocktails" exists and also that it is not empty
    cocktails = st.session_state["my_cocktails"] # the list of saved cocktails in the st.session_state is assigned to the cocktails variable

    # Display saved cocktails
    for cocktail in cocktails: # loops through all the cocktails which are expected to be dictionairies themselves
        st.subheader(cocktail["strDrink"]) # use the name of the cocktail as a title

        col1, col2, col3 = st.columns([3, 3, 3]) # we create three collumns with width = 3 parts each
        with col1:
            st.image(cocktail["strDrinkThumb"], width=200) # display the image stored in the API in form of a URL. (Size = width = 300 purely optical)

            # Calculate features
            num_ingredients, instruction_length = calculate_cocktail_features(cocktail) # run the function from data_fetch.py to get the number of ingredients and the instruction length

            # Predict difficulty using the before loaded model (line 8) and the list input of num_ingredients and instruction_length.
            prediction = model.predict([[num_ingredients, instruction_length]])[0] # the output is a single digit value 0,1,2 and we only use the first (0) prediction
            difficulty = {0: "Easy", 1: "Medium", 2: "Hard"}[prediction] # returns the diffictulty according to the prediction value as a word for the user to read


        with col2:
            st.write("**AI predicts:**")
            # Display all the cocktail details (f is used to format and ** is for bold text)
            st.write(f"Difficulty: {difficulty}") # difficulty
            st.write(f"Number of Ingredients: {num_ingredients}") # number of ingredients
            st.write(f"Instruction Length: {instruction_length} words") # instruction length

        with col3:
            st.write("**Ingredients**:") # show ingredients with their measurements
            for i in range(1, 16):
                ingredient = cocktail.get(f"strIngredient{i}")
                measurement = cocktail.get(f"strMeasure{i}")
                if ingredient:
                    st.write(f"- {measurement or ''} {ingredient}")

        st.write(f"**Instructions**: {cocktail['strInstructions']}")  # instructions for the cocktail under the image (not in a collumn)


        # Option to remove a cocktail using a button and st.session_state logic
        if st.button(f"Remove {cocktail['strDrink']} from My Cocktails", key=f"remove_{cocktail['idDrink']}"):
            st.session_state["my_cocktails"].remove(cocktail) # remove the cocktail by using st.session_state.remove
            st.success(f"{cocktail['strDrink']} removed from My Cocktails!") # display the "it-worked-Message"

    # PDF Generation Section
    st.markdown("### Generate a PDF with your favorite cocktails:") # level 3 heading (the more # the smaller the heading)
    if st.button("Generate PDF"): # initiate the button logic when clicked it has the value "True" which triggers the if-function
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:  # creates a temporary file with a unique name in the temporary directory
                                                                                    # delete = false ensures that the file does not get deleted even after the program exits
                                                                                    # as tmp_file = opens the pdf in a context manager which allows us to edit it
            # Edit the pdf with the generate_pdf logic
            generate_pdf(cocktails, tmp_file.name) # uses the list of favorite cocktails and the path to the temporary file created above as inputs and writes the information to the pdf
            st.success("PDF generated successfully!") # success message
            with open(tmp_file.name, "rb") as f:    # Opens the generated PDF file in binary read mode ("rb") to prepare it for download.
                                                    # binary mode rb is needed because text mode r would corrupt the pdf
                                                    # with function ensures that the file is properly opened and closed after use no minimize ressource usage
                st.download_button( # displays the download button allowing the user to download the pdf
                    label="Download PDF", # label of the button (name)
                    data=f, # data opened in binary mode as defined above
                    file_name="Cocktail_Shopping_List_and_Recipes.pdf", # name of the downloaded file
                    mime="application/pdf", # defines the type as PDF
                )
else:
    st.info("You haven't saved any cocktails yet.") # if there are no cocktails saved in the session state, the message is showed to the user

    



