from datetime import datetime

# Extended product catalog with more items and tiered pricing
product_catalog = {
    "Independent Print": {
        "Business Cards": {
            "inputs": ["Quantity", "Size", "Stock Type", "Coating"],
            "pricing": {500: 40, 1000: 60, 2500: 100}
        },
        "Flyers": {
            "inputs": ["Quantity", "Size", "Folding"],
            "price_per_100": 18
        },
        "Postcards": {
            "inputs": ["Quantity", "Size", "Paper Type", "Coating"],
            "pricing": {100: 25, 250: 45, 500: 65, 1000: 100}
        },
        "Brochures": {
            "inputs": ["Quantity", "Size", "Fold Type", "Paper Type"],
            "pricing": {100: 60, 250: 110, 500: 200, 1000: 350}
        },
        "Posters": {
            "inputs": ["Size", "Paper Type", "Quantity"],
            "per_unit_price": {"11x17": 10, "18x24": 15, "24x36": 25}
        },
        "Vinyl Banners": {
            "inputs": ["Size", "Grommets", "Hemming"],
            "pricing": {"2x4": 40, "3x6": 60, "4x8": 80}
        },
        "Yard Signs": {
            "inputs": ["Size", "Sides", "Quantity"],
            "price_per_unit": {"Single": 12.99, "Double": 17.99}
        },
        "Stickers": {
            "inputs": ["Size", "Shape", "Quantity", "Finish"],
            "pricing": {100: 50, 250: 100, 500: 150}
        },
        "Calendars": {
            "inputs": ["Quantity", "Size", "Binding", "Pages"],
            "pricing": {100: 300, 250: 700, 500: 1200}
        },
        "T-Shirts": {
            "inputs": ["Quantity", "Shirt Color", "Print Area", "Number of Colors"],
            "base_price_per_shirt": 10,
            "extra_color_cost": 2,
            "back_print_cost": 5
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
    info = product_catalog[business].get(product)
    if not info:
        return 0.0

    if business == "Independent Print":
        if product in ["Business Cards", "Postcards", "Brochures", "Stickers", "Calendars"]:
            qty = int(inputs.get("Quantity", 0))
            return info["pricing"].get(qty, 0.0)

        elif product == "Flyers":
            qty = int(inputs.get("Quantity", 0))
            return round((qty / 100) * info["price_per_100"], 2)

        elif product == "Posters":
            qty = int(inputs.get("Quantity", 0))
            size = inputs.get("Size", "11x17")
            return qty * info["per_unit_price"].get(size, 0)

        elif product == "Vinyl Banners":
            size = inputs.get("Size", "2x4")
            return info["pricing"].get(size, 0.0)

        elif product == "Yard Signs":
            qty = int(inputs.get("Quantity", 0))
            sides = inputs.get("Sides", "Single")
            unit_price = info["price_per_unit"].get(sides, 12.99)
            return round(qty * unit_price, 2)

        elif product == "T-Shirts":
            qty = int(inputs.get("Quantity", 0))
            colors = int(inputs.get("Number of Colors", 1))
            area = inputs.get("Print Area", "Front")
            base = info["base_price_per_shirt"]
            extra_color_cost = (colors - 1) * info["extra_color_cost"]
            back = info["back_print_cost"] if area == "Both" else 0
            return round(qty * (base + extra_color_cost + back), 2)

    elif business == "Independent Wraps":
        if product == "Full Wrap":
            sqft = float(inputs.get("Sq Ft", 0))
            multiplier = 1.2 if inputs.get("Complexity", "Normal") == "Complex" else 1.0
            return round(sqft * info["base_price_per_sqft"] * multiplier, 2)

        elif product == "Window Perf":
            sqft = float(inputs.get("Area (Sq Ft)", 0))
            price = sqft * info["price_per_sqft"]
            if inputs.get("Laminate?", "No") == "Yes":
                price += sqft * 2
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
