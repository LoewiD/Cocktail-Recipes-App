from fpdf import FPDF
import os


class PDF(FPDF):
    def header(self):
        # Set font and add a header title
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Cocktail Shopping List & Recipes", align="C", ln=1)

    def add_shopping_list(self, ingredients):
        self.add_page()
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Shopping List", ln=1)
        self.set_font("Arial", "", 12)
        self.ln(10)

        for ingredient in ingredients:
            self.cell(0, 10, f"- {ingredient}", ln=1)

    def add_cocktail_details(self, cocktail):
        self.add_page()
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, cocktail["strDrink"], ln=1)
        self.ln(5)

        # Add Image (if available)
        if cocktail["strDrinkThumb"]:
            img_path = f'tmp/{cocktail["idDrink"]}.jpg'
            self.add_image_from_url(cocktail["strDrinkThumb"], img_path, 80, 60, 80)

        # Ingredients and measurements
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Ingredients:", ln=1)
        self.set_font("Arial", "", 12)
        for i in range(1, 16):
            ingredient = cocktail.get(f"strIngredient{i}")
            measurement = cocktail.get(f"strMeasure{i}")
            if ingredient:
                self.cell(0, 10, f"- {measurement or ''} {ingredient}".strip(), ln=1)

        # Instructions
        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Instructions:", ln=1)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, cocktail["strInstructions"])

    def add_image_from_url(self, url, save_path, x, y, width):
        try:
            import requests
            from PIL import Image
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                self.image(save_path, x=x, y=y, w=width)
                os.remove(save_path)
        except Exception as e:
            print(f"Failed to add image: {e}")


def generate_pdf(cocktails, save_path):
    pdf = PDF()

    # Extract unique ingredients for the shopping list
    unique_ingredients = set()
    for cocktail in cocktails:
        for i in range(1, 16):
            ingredient = cocktail.get(f"strIngredient{i}")
            if ingredient:
                unique_ingredients.add(ingredient)

    # Add Shopping List to PDF
    pdf.add_shopping_list(sorted(unique_ingredients))

    # Add each cocktail's details to PDF
    for cocktail in cocktails:
        pdf.add_cocktail_details(cocktail)

    # Output the PDF
    pdf.output(save_path)
