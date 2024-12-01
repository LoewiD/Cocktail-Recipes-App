from fpdf import FPDF
import os


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 128, 47)  # Green (matching graphs in data visualization)
        self.cell(0, 10, "Cocktail Shopping List & Recipes", align="C", ln=1)
        self.ln(5)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.5)
        self.line(10, 20, 200, 20)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_shopping_list(self, ingredients):
        self.add_page()
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 128, 47)  # Green
        self.cell(0, 10, "Shopping List", ln=1, align="C")
        self.ln(10)

        self.set_font("Arial", "", 12)
        self.set_text_color(0, 0, 0)
        for ingredient in ingredients:
            self.cell(0, 10, f"- {ingredient}", ln=1)

    def add_cocktail_details(self, cocktail):
        self.add_page()
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 128, 47)  # Green
        self.cell(0, 10, cocktail["strDrink"], ln=1, align="C")
        self.ln(10)

        # Add Cocktail Image
        image_height = 70  # Default height for spacing
        if cocktail.get("strDrinkThumb"):
            img_path = f'tmp/{cocktail["idDrink"]}.jpg'
            image_height = self.add_image_from_url(cocktail["strDrinkThumb"], img_path, 65, 40, 80)
            self.ln(image_height + 10)  # Add spacing below the image

        # Ingredients Section
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 128, 47)  # Green
        self.cell(0, 10, "Ingredients:", ln=1, align="C")
        self.ln(5)

        self.set_font("Arial", "", 12)
        self.set_text_color(0, 0, 0)
        for i in range(1, 16):
            ingredient = cocktail.get(f"strIngredient{i}")
            measurement = cocktail.get(f"strMeasure{i}")
            if ingredient:
                self.cell(0, 10, f"{measurement or ''} {ingredient}".strip(), ln=1, align="C")

        # Instructions Section
        self.ln(15)  # Ensure adequate spacing from the ingredients
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 128, 47)  # Green
        self.cell(0, 10, "Instructions:", ln=1, align="C")
        self.ln(5)

        self.set_font("Arial", "", 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 10, cocktail["strInstructions"], align="C")

    def add_image_from_url(self, url, save_path, x, y, width):
        # Fetch and add an image from a URL
        try:
            import requests
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                img = self.image(save_path, x=x, y=y, w=width)
                os.remove(save_path)
                return 80  # Return approximate image height
            else:
                print(f"Failed to fetch image from {url}, status code: {response.status_code}")
                return 0  # No image
        except Exception as e:
            print(f"Error while adding image: {e}")
            return 0  # No image


def generate_pdf(cocktails, save_path):
    pdf = PDF()

    # Create tmp directory if it doesn't exist
    os.makedirs("tmp", exist_ok=True)

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

    # Clean up tmp directory after PDF generation
    for file in os.listdir("tmp"):
        os.remove(os.path.join("tmp", file))

    # Output the PDF
    pdf.output(save_path)
