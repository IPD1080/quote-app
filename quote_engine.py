from datetime import datetime

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
        "Stretched Canvas Prints": {
            "inputs": ["Quantity", "Size"],
            "pricing": {"12x12": 20, "16x20": 35, "24x36": 60}
        },
        "Window Clings": {
            "inputs": ["Quantity", "Size"],
            "pricing": {"12x18": 10, "18x24": 15, "24x36": 25}
        },
        "Wall Decals": {
            "inputs": ["Size", "Material"],
            "pricing": {"24x24": 40, "36x36": 65, "48x48": 90}
        },
        "Calendars": {
            "inputs": ["Quantity", "Size", "Binding", "Pages"],
            "pricing": {100: 300, 250: 700, 500: 1200}
        },
        "T-Shirts": {
            "inputs": ["Quantity", "Shirt Color", "Print Area", "Number of Colors"],
            "base_price_per_unit": 10,
            "extra_color_cost": 2,
            "back_print_cost": 5
        }
    },
    "Independent Wraps": {
        "Full Wrap": {
            "inputs": ["Vehicle Type", "Sq Ft", "Complexity"],
            "base_price_per_sqft": 12
        },
        "Partial Wrap": {
            "inputs": ["Sq Ft"],
            "base_price_per_sqft": 14
        },
        "Spot Graphics": {
            "inputs": ["Graphic Count"],
            "price_per_graphic": 35
        },
        "Vehicle Lettering": {
            "inputs": ["Font Type", "Color", "Text Length"],
            "base_price": 150
        },
        "Window Decals": {
            "inputs": ["Size"],
            "pricing": {"12x18": 35, "18x24": 50, "24x36": 70}
        },
        "Fleet Graphics": {
            "inputs": ["Vehicle Count"],
            "base_price_per_vehicle": 650
        },
        "Color Change Wrap": {
            "inputs": ["Vehicle Type"],
            "pricing": {"Car": 2200, "SUV": 2500, "Truck": 2800}
        },
        "Chrome Delete": {
            "inputs": ["Parts"],
            "price_per_part": 75
        },
        "Roof Wrap": {
            "inputs": ["Size"],
            "pricing": {"Small": 250, "Medium": 350, "Large": 450}
        },
        "Hood Wrap": {
            "inputs": ["Size"],
            "pricing": {"Small": 200, "Medium": 300, "Large": 400}
        },
        "Racing Stripes": {
            "inputs": ["Length"],
            "price_per_foot": 25
        },
        "Carbon Fiber Accents": {
            "inputs": ["Part"],
            "base_price": 150
        },
        "Paint Protection Film": {
            "inputs": ["Panel Count"],
            "price_per_panel": 120
        },
        "Reflective Wrap": {
            "inputs": ["Sq Ft"],
            "price_per_sqft": 18
        },
        "Finish Options": {
            "inputs": ["Finish"],
            "pricing": {"Gloss": 0, "Matte": 150, "Satin": 200, "Color Flip": 300}
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
        qty = int(inputs.get("Quantity", 0))
        if "pricing" in info:
            if isinstance(info["pricing"], dict):
                size = inputs.get("Size")
                return info["pricing"].get(qty, info["pricing"].get(size, 0.0))
        elif "price_per_100" in info:
            return round((qty / 100) * info["price_per_100"], 2)
        elif product == "T-Shirts":
            colors = int(inputs.get("Number of Colors", 1))
            area = inputs.get("Print Area", "Front")
            base = info["base_price_per_unit"]
            extra = (colors - 1) * info["extra_color_cost"]
            back = info["back_print_cost"] if area == "Both" else 0
            return round(qty * (base + extra + back), 2)

    elif business == "Independent Wraps":
        if product == "Full Wrap":
            sqft = float(inputs.get("Sq Ft", 0))
            multiplier = 1.2 if inputs.get("Complexity", "Normal") == "Complex" else 1.0
            return round(sqft * info["base_price_per_sqft"] * multiplier, 2)
        elif product in ["Partial Wrap", "Reflective Wrap"]:
            sqft = float(inputs.get("Sq Ft", 0))
            return round(sqft * info["price_per_sqft"] if "price_per_sqft" in info else info["base_price_per_sqft"], 2)
        elif product == "Spot Graphics":
            count = int(inputs.get("Graphic Count", 0))
            return round(count * info["price_per_graphic"], 2)
        elif product == "Vehicle Lettering":
            return info["base_price"]
        elif product == "Window Decals":
            size = inputs.get("Size", "")
            return info["pricing"].get(size, 0.0)
        elif product == "Fleet Graphics":
            count = int(inputs.get("Vehicle Count", 0))
            return count * info["base_price_per_vehicle"]
        elif product == "Color Change Wrap":
            vtype = inputs.get("Vehicle Type", "")
            return info["pricing"].get(vtype, 0.0)
        elif product == "Chrome Delete":
            parts = int(inputs.get("Parts", 0))
            return parts * info["price_per_part"]
        elif product in ["Roof Wrap", "Hood Wrap"]:
            size = inputs.get("Size", "")
            return info["pricing"].get(size, 0.0)
        elif product == "Racing Stripes":
            length = float(inputs.get("Length", 0))
            return round(length * info["price_per_foot"], 2)
        elif product == "Carbon Fiber Accents":
            return info["base_price"]
        elif product == "Paint Protection Film":
            count = int(inputs.get("Panel Count", 0))
            return count * info["price_per_panel"]
        elif product == "Finish Options":
            finish = inputs.get("Finish", "Gloss")
            return info["pricing"].get(finish, 0.0)

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
