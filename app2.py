import json
from reportlab.pdfgen import canvas

def convert_json_to_pdf(json_file, pdf_file):
    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Create PDF canvas
    c = canvas.Canvas(pdf_file)

    # Set font and font size
    c.setFont("Helvetica", 12)

    # Write JSON data to PDF
    for key, value in data.items():
        c.drawString(50, 700, f"{key}: {value}")
        c.showPage()

    # Save PDF file
    c.save()

# Example usage
json_file = 'jeedata.json'
pdf_file = 'data/jeedata.pdf'
convert_json_to_pdf(json_file, pdf_file)