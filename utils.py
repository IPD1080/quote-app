
import csv
import pdfkit
from pathlib import Path

def save_quote_to_csv(quote, filename='quotes.csv'):
    fieldnames = list(quote["Inputs"].keys()) + list(quote["Outputs"].keys()) + ["Business", "Created"]
    data = {**quote["Inputs"], **quote["Outputs"]}
    data["Business"] = quote.get("System", {}).get("Business", "Unknown")
    data["Created"] = quote.get("System", {}).get("Created", "")

    file_exists = Path(filename).exists()
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def export_quote_to_pdf(quote_data, filename="quote.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Draw logo at top left
    try:
        logo = ImageReader("IPD LOGO.png")
        c.drawImage(logo, 50, height - 120, width=120, preserveAspectRatio=True, mask='auto')
    except:
        pass

    # Add company contact info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(200, height - 60, "Independent Print & Design")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 75, "1080 Holland Drive, Suite 3")
    c.drawString(200, height - 90, "Boca Raton, FL 33487")
    c.drawString(200, height - 105, "Phone: 561-223-1111")
    c.drawString(200, height - 120, "orders@independentprint.com")

    # Quote info
    y = height - 160
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"Quote for: {quote_data['Inputs'].get('Customer Name', 'Customer')}")
    y -= 20

    for key, value in quote_data["Outputs"].items():
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"{key}: ${value}")
        y -= 15

    c.save()
    customer = quote["Inputs"].get("Customer Name", "Customer")
    html = f"""
    <html><head><style>
    body {{ font-family: Arial, sans-serif; }}
    h1 {{ color: #333; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    </style></head><body>
    <h1>Quote for {customer}</h1>
    <h2>Quote Breakdown</h2>
    <table>
        <tr><th>Item</th><th>Amount</th></tr>
        {''.join(f'<tr><td>{key}</td><td>${value}</td></tr>' for key, value in quote['Outputs'].items())}
    </table>
    <p><strong>Total:</strong> ${quote['Outputs'].get('Total Estimate', 0)}</p>
    </body></html>
    """
    pdfkit.from_string(html, filename)
