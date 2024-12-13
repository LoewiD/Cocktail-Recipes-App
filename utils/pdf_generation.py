from fpdf import FPDF # library used to create and manage the PDF document. It provides methods to add pages, set fonts, write text, insert images etc..
import os   # Python os module, which provides functionalit for interacting with the operating system
            # such as file management and directory handling


class PDF(FPDF): # create custom PDF class that extends the FPDF functionality (to define headers and footers for example)
    def header(self): # defines the header of the PDF by redefining the FPDF Class
        self.set_font("Arial", "B", 16) # Sets the font to Arial, makes it bold, and sets the size to 16
        self.set_text_color(0, 128, 47)  # Green (matching graphs in data visualization, HSG green)
        self.cell(0, 10, "Cocktail Shopping List & Recipes", align="C", ln=1)   # Adds a centered header title "Cocktail Shopping List & Recipes" on the page
                                                    # 0: Full page width, 10: Height of the cell, align="C": Center alignment, ln=1: Moves to the next line after writing
        self.ln(5) # Adds a vertical line break (spacing) of 5 units below the title
        self.set_draw_color(200, 200, 200) # Sets the color for the line to light gray (RGB: 200, 200, 200)
        self.set_line_width(0.5) # Sets the thickness of the line to 0.5 units
        self.line(10, 20, 200, 20) # Draws a horizontal line from (10, 20) to (200, 20) to visually separate the header from the content below.

    def footer(self):  # Defines the footer of the PDF by redefining the FPDF Class
        self.set_y(-15)  # Sets the vertical position of the footer 15 units from the bottom of the page
        self.set_font("Arial", "I", 10)  # Sets the font to Arial, makes it italic, and sets the size to 10
        self.set_text_color(128, 128, 128)  # Sets the text color to gray (RGB: 128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")  # Adds a centered footer displaying the current page number
        # 0: Full page width, 10: Height of the cell, align="C": Center alignment

    def add_shopping_list(self, ingredients):  # Defines a method to add a shopping list page to the PDF
        self.add_page()  # Adds a new page to the PDF for the shopping list
        self.set_font("Arial", "B", 16)  # Sets the font to Arial, makes it bold, and sets the size to 16
        self.set_text_color(0, 128, 47)  # Sets the text color to green (HSG green, matching the theme)
        self.cell(0, 10, "Shopping List", ln=1, align="C")  # Adds a centered title "Shopping List" on the page
        # 0: Full page width, 10: Height of the cell, ln=1: Moves to the next line after writing, align="C": Center alignment
        self.ln(10)  # Adds a vertical line break (spacing) of 10 units below the title

        self.set_font("Arial", "",12)  # Sets the font to Arial, regular style (not bold or italic), and size 12 for the list items
        self.set_text_color(0, 0, 0)  # Sets the text color to black (RGB: 0, 0, 0)
        for ingredient in ingredients:  # Loops through the list of ingredients to add each one to the PDF
            self.cell(0, 10, f"- {ingredient}", ln=1)  # Adds each ingredient as a new line prefixed with a dash ("-")
            # 0: Full page width, 10: Height of the cell, ln=1: Moves to the next line after writing

    def add_cocktail_details(self, cocktail):  # Defines a method to add details of a single cocktail to the PDF
        self.add_page()  # Adds a new page to the PDF for the cocktail details
        self.set_font("Arial", "B",16)  # Sets the font to Arial, makes it bold, and sets the size to 16 for the cocktail title
        self.set_text_color(0, 128, 47)  # Sets the text color to green (HSG green, matching the theme).
        self.cell(0, 10, cocktail["strDrink"], ln=1, align="C")  # Adds the cocktail's name as a centered title on the page
        # 0: Full page width, 10: Height of the cell, ln=1: Moves to the next line after writing, align="C": Center alignment
        self.ln(10)  # Adds a vertical line break (spacing) of 10 units below the cocktail title

        # Add Cocktail Image
        image_height = 70  # Sets a default height for spacing in case the image is not available
        if cocktail.get("strDrinkThumb"):  # Checks if the cocktail has a thumbnail image URL
            img_path = f'tmp/{cocktail["idDrink"]}.jpg'  # Defines the temporary path to save the downloaded image locally
            image_height = self.add_image_from_url(cocktail["strDrinkThumb"], img_path, 65, 40, 80)
            # Downloads the image from the URL, saves it temporarily, and adds it to the PDF
            # 65: X-coordinate, 40: Y-coordinate, 80: Image width
            self.ln(image_height + 10)  # Adds vertical spacing below the image, based on its height plus 10 units

        # Ingredients Section
        self.set_font("Arial", "B",14)  # Sets the font to Arial, makes it bold, and sets the size to 14 for the section title
        self.set_text_color(0, 128, 47)  # Sets the text color to green (HSG green, matching the theme)
        self.cell(0, 10, "Ingredients:", ln=1, align="C")  # Adds a centered section title "Ingredients" to the page
        # 0: Full page width, 10: Height of the cell, ln=1: Moves to the next line after writing, align="C": Center alignment
        self.ln(5)  # Adds a vertical line break (spacing) of 5 units below the title

        self.set_font("Arial", "", 12)  # Sets the font to Arial, regular style (not bold or italic), and size 12 for the list items
        self.set_text_color(0, 0, 0)  # Sets the text color to black (RGB: 0, 0, 0).
        for i in range(1, 16):  # Loops through possible ingredient and measurement pairs (maximum of 15 pairs)
            ingredient = cocktail.get(f"strIngredient{i}")  # Retrieves the ingredient name for the current index
            measurement = cocktail.get(f"strMeasure{i}")  # Retrieves the measurement for the current index
            if ingredient:  # Checks if the ingredient exists
                self.cell(0, 10, f"{measurement or ''} {ingredient}".strip(), ln=1, align="C")
                # Adds the measurement and ingredient name as a centered line in the PDF
                # If measurement is None, it defaults to an empty string
                # 0: Full page width, 10: Height of the cell, ln=1: Moves to the next line after writing, align="C": Center alignment

        # Instructions Section
        self.ln(15)  # Adds a vertical line break (spacing) of 15 units to ensure adequate spacing from the ingredients section
        self.set_font("Arial", "B",14)  # Sets the font to Arial, makes it bold, and sets the size to 14 for the section title
        self.set_text_color(0, 128, 47)  # Sets the text color to green (HSG green, matching the theme)
        self.cell(0, 10, "Instructions:", ln=1, align="C")  # Adds a centered section title "Instructions" to the page
        # 0: Full page width, 10: Height of the cell, ln=1: Moves to the next line after writing, align="C": Center alignment
        self.ln(5)  # Adds a vertical line break (spacing) of 5 units below the title

        self.set_font("Arial", "", 12)  # Sets the font to Arial, regular style (not bold or italic), and size 12 for the instructions text
        self.set_text_color(0, 0, 0)  # Sets the text color to black (RGB: 0, 0, 0)
        self.multi_cell(0, 10, cocktail["strInstructions"], align="C")   # Adds the instructions text as multiple lines, centered
                                     # 0: Full page width, 10: Height of each line, align="C": Center alignment for all lines

    def add_image_from_url(self, url, save_path, x, y, width): #self ensures that changes made within this method apply to the specific PDF object being worked on, not a generic one
        # Fetch and add an image from a URL
        try:
            import requests
            response = requests.get(url, stream=True) #instructs the requests library to download the content incrementally (in chunks) instead of loading it all at once into memory
            if response.status_code == 200: # OK
                with open(save_path, "wb") as f: # opens file specified by save_path in binary write mode (wb) to ensure the data is read as it is on the server
                    f.write(response.content) # saves the downloaded image to the local system at the specified save_path (in binary).
                img = self.image(save_path, x=x, y=y, w=width) # Adds the image saved at save_path to the PDF
                os.remove(save_path) # Deletes the temporary image file from the local system after it has been added to the PDF
                return 80  # Return approximate image height (This value is used to calculate additional spacing between sections)
            else:
                print(f"Failed to fetch image from {url}, status code: {response.status_code}") # error message
                return 0  # No image, ensures no unnessesary spacing is put in the pdf
        except Exception as e: # catches exceptions (network related issues)
            print(f"Error while adding image: {e}")
            return 0  # No image


def generate_pdf(cocktails, save_path): # function to save PDFs
    pdf = PDF() # initializes the PDF object so that we can use FPDF logic


    os.makedirs("tmp", exist_ok=True) # chekcs for the tmp folder directory and creates it if it does not exist, exist_ok=True is there to prevent an error if there is already a tmp folder

    # Extract unique ingredients for the shopping list
    unique_ingredients = set() # Initializes an empty set to store unique ingredients (A set automatically removes duplicates)
    for cocktail in cocktails: # loops through the cocktail list
        for i in range(1, 16): # goes through the 15 possible ingredients in the cocktails
            ingredient = cocktail.get(f"strIngredient{i}") # gets the current ingredient
            if ingredient: # checks for ingredient
                unique_ingredients.add(ingredient) # Adds it to the set to ensure no duplicates


    pdf.add_shopping_list(sorted(unique_ingredients)) # Adds the sorted list of unique ingredients to the PDF

    for cocktail in cocktails: # loop through the cocktail list
        pdf.add_cocktail_details(cocktail) # add cocktail details to the pdf

    # Clean up tmp directory after PDF generation
    for file in os.listdir("tmp"): # Loops through all files in the tmp directory
        os.remove(os.path.join("tmp", file)) # Deletes each file in the directory (after joining them all together)

    # Output the PDF
    pdf.output(save_path) # Writes the final PDF to the specified "save_path"


