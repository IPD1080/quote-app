
from datetime import datetime

# Product catalog with inputs and pricing logic
product_catalog = {
    "Independent Print": {
        "Business Cards": {
            "inputs": ["Quantity", "Size", "Stock Type", "Coating"],
            "pricing": {500: 40, 1000: 60, 2500: 100}
        },
        "Flyers": {
            "inputs": ["Quantity", "Size", "Folding"],
            "price_per_100": 18
        }
    },
    "Independent Wraps": {
        "Full Wrap": {
            "inputs": ["Vehicle Type", "Sq Ft", "Complexity"],
            "base_price_per_sqft": 12
        },
        "Window Perf": {
            "inputs": ["Area (Sq Ft)", "Laminate?"],
            "price_per_sqft": 8
        }
    }
}

def create_base_quote(business='Independent Print'):
    return {
        "Business": business,
        "Inputs": {},
        "Outputs": {
            "Product": "",
            "Base Cost": 0.0,
            "Add-ons": 0.0,
            "Tax": 0.0,
            "Total Estimate": 0.0
        },
        "System": {
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": "Draft"
        }
    }

def calculate_product_price(business, product, inputs):
    if business not in product_catalog or product not in product_catalog[business]:
        return 0.0

    info = product_catalog[business][product]

    if business == "Independent Print":
        if product == "Business Cards":
            qty = int(inputs.get("Quantity", 0))
            return info["pricing"].get(qty, 0.0)
        elif product == "Flyers":
            qty = int(inputs.get("Quantity", 0))
            return round((qty / 100) * info["price_per_100"], 2)

    elif business == "Independent Wraps":
        if product == "Full Wrap":
            sqft = float(inputs.get("Sq Ft", 0))
            complexity = inputs.get("Complexity", "Normal")
            multiplier = 1.2 if complexity == "Complex" else 1.0
            return round(sqft * info["base_price_per_sqft"] * multiplier, 2)
        elif product == "Window Perf":
            sqft = float(inputs.get("Area (Sq Ft)", 0))
            laminate = inputs.get("Laminate?", "No")
            price = sqft * info["price_per_sqft"]
            if laminate == "Yes":
                price += sqft * 2  # $2 per sq ft for laminate
            return round(price, 2)

    return 0.0

def calculate_quote(quote):
    business = quote["Business"]
    product = quote["Inputs"].get("Product", "")
    inputs = quote["Inputs"]
    base_cost = calculate_product_price(business, product, inputs)
    tax = base_cost * 0.07
    total = base_cost + tax

    quote["Outputs"]["Product"] = product
    quote["Outputs"]["Base Cost"] = round(base_cost, 2)
    quote["Outputs"]["Tax"] = round(tax, 2)
    quote["Outputs"]["Total Estimate"] = round(total, 2)

    return quote
