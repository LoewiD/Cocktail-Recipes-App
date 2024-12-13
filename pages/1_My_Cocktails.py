import streamlit as st  # use streamlit
from utils.data_fetch import calculate_cocktail_features  # we need the data_fetch script for the calculate_cocktail_features function
from utils.pdf_generation import generate_pdf  # we need the pdf logic to create the pdf button
import joblib  # Handles saving and loading Python objects efficiently. we need it to import our pre-trained ML model
import tempfile  # Creates temporary files and directories that are automatically deleted when no longer needed.
                # we use it to create a temporary PDF for the user to download while not cluttering the file system

### Delete the lower two ### to check sklearn version if we have an error
### import sklearn
### st.write(sklearn.__version__)

# Load the pre-trained ML model using joblib (we have to have it trained Manually before!)
model = joblib.load("ml/difficulty_model.pkl")

# Page Title
st.title("🍹 My Cocktails")

# Check if there are saved cocktails. St.session_state is a special dictionary-like object in Streamlit used to persist data across app reruns.
if "my_cocktails" in st.session_state and st.session_state["my_cocktails"]:  # checks that the key "my_cocktails" exists and also that it is not empty
    cocktails = st.session_state["my_cocktails"]  # the list of saved cocktails in the st.session_state is assigned to the cocktails variable

    st.info("""
    ### Tips for Difficulty Levels:
    - **Easy**: Minimal ingredients, short/simple instructions.
    - **Moderate**: Moderate ingredients and complexity.
    - **Hard**: Many ingredients or detailed preparation steps.
    """)

    # Display saved cocktails
    for cocktail in cocktails:  # loops through all the cocktails which are expected to be dictionaries themselves
        st.subheader(cocktail["strDrink"])  # use the name of the cocktail as a title

        col1, col2, col3 = st.columns([3, 3, 3])  # we create three columns with width = 3 parts each
        with col1:
            st.image(cocktail["strDrinkThumb"], width=200)  # display the image stored in the API in form of a URL. (Size = width = 300 purely optical)

            # Calculate features
            num_ingredients, instruction_length = calculate_cocktail_features(cocktail)  # run the function from data_fetch.py to get the number of ingredients and the instruction length

            # Additional feature calculations
            ingredients = [cocktail.get(f"strIngredient{i}") for i in range(1, 16)]  # list of all ingredients
            measures = [cocktail.get(f"strMeasure{i}") for i in range(1, 16)]  # list of all measurements

            # Count the number of measurements used
            num_measurements = len([meas for meas in measures if meas])

            # Calculate preparation complexity based on specific keywords in the instructions
            complex_keywords = ['shake', 'blend', 'layer', 'strain', 'stir', 'muddle']
            preparation_complexity = sum(1 for keyword in complex_keywords if keyword in cocktail.get("strInstructions", "").lower())

            # Fetch other complexities from cocktail dictionary or set default values if not present
            ingredient_complexity = cocktail.get("ingredient_complexity", 3)  # Default to moderate complexity if missing
            instruction_complexity = cocktail.get("instruction_complexity", 3)
            tool_complexity = cocktail.get("tool_complexity", 3)
            glass_type_complexity = cocktail.get("glass_type_complexity", 2)

            # Combine all features to form input for prediction
            features = [
                num_ingredients,
                instruction_length,
                num_measurements,
                preparation_complexity,
                ingredient_complexity,
                instruction_complexity,
                tool_complexity,
                glass_type_complexity
            ]

            # Predict difficulty using the before loaded model (line 8) and the list input of all 8 features.
            prediction = model.predict([features])[0]  # the output is a label value (Easy, Moderate, Hard)
            difficulty = {"Easy": "Easy", "Moderate": "Moderate", "Hard": "Hard"}[prediction]  # returns the difficulty according to the prediction value as a word for the user to read

        with col2:
            st.write("**AI predicts:**")
            # Display all the cocktail details (f is used to format and ** is for bold text)
            st.write(f"Difficulty: {difficulty}")  # difficulty
            st.write(f"Number of Ingredients: {num_ingredients}")  # number of ingredients
            st.write(f"Instruction Length: {instruction_length} words")  # instruction length


        with col3:
            st.write("**Ingredients**:")  # show ingredients with their measurements
            for i in range(1, 16):
                ingredient = cocktail.get(f"strIngredient{i}")
                measurement = cocktail.get(f"strMeasure{i}")
                if ingredient:
                    st.write(f"- {measurement or ''} {ingredient}")

        st.write(f"**Instructions**: {cocktail['strInstructions']}")  # instructions for the cocktail under the image (not in a column)

        # Option to remove a cocktail using a button and st.session_state logic
        if st.button(f"Remove {cocktail['strDrink']} from My Cocktails", key=f"remove_{cocktail['idDrink']}"): # every widget in streamlit need to have a specific key so that the app knows what cocktail to delete
            st.session_state["my_cocktails"].remove(cocktail)  # remove the cocktail by using st.session_state.remove
            st.success(f"{cocktail['strDrink']} removed from My Cocktails!")  # display the "it-worked" message

    # PDF Generation Section
    st.markdown("### Generate a PDF with your favorite cocktails:")  # level 3 heading (the more # the smaller the heading)
    if st.button("Generate PDF"):  # initiate the button logic when clicked it has the value "True" which triggers the if-function
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:  # creates a temporary file with a unique name in the temporary directory (tmp as standard)
            # delete = false ensures that the file does not get deleted even after the program exits
            # as tmp_file = opens the pdf in a context manager which allows us to edit it
            # Edit the pdf with the generate_pdf logic
            generate_pdf(cocktails, tmp_file.name)  # uses the list of favorite cocktails and the path to the temporary file created above as inputs and writes the information to the pdf
            st.success("PDF generated successfully!")  # success message
            with open(tmp_file.name, "rb") as f:  # Opens the generated PDF file in binary read mode ("rb") to prepare it for download.
                # binary mode rb is needed because text mode r would corrupt the pdf
                # with function ensures that the file is properly opened and closed after use to minimize resource usage
                st.download_button(  # displays the download button allowing the user to download the pdf
                    label="Download PDF",  # label of the button (name)
                    data=f,  # data opened in binary mode as defined above
                    file_name="Cocktail_Shopping_List_and_Recipes.pdf",  # name of the downloaded file
                    mime="application/pdf",  # defines the type as PDF which allows the browser to interpret the binary file as a pdf to show it correctly to the user
                )
else:
    st.info("You haven't saved any cocktails yet.")  # if there are no cocktails saved in the session state, the message is showed to the user

