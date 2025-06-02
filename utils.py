
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

def export_quote_to_pdf(quote, filename='quote.pdf'):
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
