from datetime import datetime

product_catalog = {
    "Independent Print": {
        "Business Cards": {
            "inputs": ["Quantity", "Sides", "Paper Type", "Finish"],
            "price_per_100": 12.00
        },
        "Flyers": {
            "inputs": ["Quantity", "Size", "Paper Type", "Coating", "Sides"],
            "price_per_100": 15.00
        },
        "Brochures": {
            "inputs": ["Quantity", "Size", "Paper Type", "Fold Type", "Coating"],
            "price_per_100": 20.00
        },
        "Postcards": {
            "inputs": ["Quantity", "Size", "Paper Type", "Coating", "Sides"],
            "price_per_100": 14.00
        },
        "Booklets": {
            "inputs": ["Quantity", "Size", "Paper Type", "Binding"],
            "price_per_100": 40.00
        },
        "Posters": {
            "inputs": ["Quantity", "Size", "Paper Type", "Finish"],
            "price_per_100": 25.00
        },
        "Stickers": {
            "inputs": ["Quantity", "Size", "Shape", "Finish"],
            "price_per_100": 18.00
        },
        "Banners": {
            "inputs": ["Size", "Grommets", "Hemming"],
            "pricing": {
                "2x4": 30.00,
                "3x6": 45.00,
                "4x8": 60.00
            }
        },
        "Yard Signs": {
            "inputs": ["Quantity", "Size", "Sides"],
            "price_per_100": 60.00
        },
        "Canvas Prints": {
            "inputs": ["Quantity", "Size"],
            "pricing": {
                "12x12": 35.00,
                "16x20": 45.00,
                "12x18": 40.00,
                "36x48": 80.00
            }
        },
        "Window Clings": {
            "inputs": ["Quantity", "Size"],
            "pricing": {
                "18x24": 20.00,
                "24x36": 30.00
            }
        },
        "Wall Decals": {
            "inputs": ["Size", "Shape", "Material"],
            "pricing": {
                "24x36": 28.00,
                "36x48": 40.00
            }
        },
        "Apparel": {
            "inputs": ["Quantity", "Print Area", "Number of Colors"],
            "base_price_per_unit": 9.00,
            "extra_color_cost": 1.50,
            "back_print_cost": 4.00
        }
    },

    "Independent Wraps": {
        "Spot Graphics": {
            "inputs": ["Graphic Count", "Material"],
            "price_per_graphic": 75.00
        },
        "Vehicle Lettering": {
            "inputs": ["Text Length", "Font Type", "Color"],
            "base_price": 250.00
        },
        "Window Decals": {
            "inputs": ["Size", "Laminate?"],
            "pricing": {
                "18x24": 55.00,
                "24x36": 75.00
            }
        },
        "Fleet Graphics": {
            "inputs": ["Vehicle Count", "Complexity"],
            "base_price_per_vehicle": 900.00
        },
        "Color Change Wrap": {
            "inputs": ["Vehicle Type", "Finish"],
            "pricing": {
                "Sedan": 2200.00,
                "SUV": 2600.00,
                "Truck": 2800.00
            }
        },
        "Chrome Delete": {
            "inputs": ["Parts"],
            "price_per_part": 50.00
        },
        "Partial Wrap": {
            "inputs": ["Sq Ft", "Include Laminate"],
            "base_price_per_sqft": 18.00
        },
        "Roof Wrap": {
            "inputs": ["Size"],
            "pricing": {
                "4x4": 180.00,
                "5x5": 225.00
            }
        },
        "Hood Wrap": {
            "inputs": ["Size"],
            "pricing": {
                "4x4": 160.00,
                "5x5": 200.00
            }
        },
        "Racing Stripes": {
            "inputs": ["Length", "Color"],
            "price_per_foot": 18.00
        },
        "Carbon Fiber Accents": {
            "inputs": ["Item Type"],
            "base_price": 125.00
        },
        "Paint Protection Film": {
            "inputs": ["Panel Count"],
            "price_per_panel": 95.00
        },
        "Reflective Wrap": {
            "inputs": ["Sq Ft"],
            "price_per_sqft": 25.00
        },
        "Finish Options": {
            "inputs": ["Finish"],
            "pricing": {
                "Gloss": 0.00,
                "Matte": 150.00,
                "Satin": 150.00,
                "Color Flip": 300.00
            }
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

    qty = int(inputs.get("Quantity", 0))
    sqft = float(inputs.get("Sq Ft", 0))
    size = inputs.get("Size", "")
    pricing = info.get("pricing", {})

    if business == "Independent Print":
        if "price_per_100" in info:
            return round((qty / 100) * info["price_per_100"], 2)
        elif product in ["Canvas Prints", "Window Clings", "Wall Decals"]:
            return pricing.get(size, 0.0) * qty
        elif product == "Apparel":
            colors = int(inputs.get("Number of Colors", 1))
            area = inputs.get("Print Area", "Front")
            base = info["base_price_per_unit"]
            extra = (colors - 1) * info["extra_color_cost"]
            back = info["back_print_cost"] if area == "Both" else 0
            return round(qty * (base + extra + back), 2)
        elif "pricing" in info:
            return pricing.get(size, 0.0)

    elif business == "Independent Wraps":
        if product == "Spot Graphics":
            return int(inputs.get("Graphic Count", 0)) * info["price_per_graphic"]
        elif product == "Vehicle Lettering":
            return info["base_price"]
        elif product in ["Window Decals", "Roof Wrap", "Hood Wrap"]:
            return pricing.get(size, 0.0)
        elif product == "Fleet Graphics":
            return int(inputs.get("Vehicle Count", 0)) * info["base_price_per_vehicle"]
        elif product == "Color Change Wrap":
            vtype = inputs.get("Vehicle Type", "")
            return pricing.get(vtype, 0.0)
        elif product == "Chrome Delete":
            return int(inputs.get("Parts", 0)) * info["price_per_part"]
        elif product == "Partial Wrap":
            return sqft * info["base_price_per_sqft"]
        elif product == "Racing Stripes":
            return float(inputs.get("Length", 0)) * info["price_per_foot"]
        elif product == "Carbon Fiber Accents":
            return info["base_price"]
        elif product == "Paint Protection Film":
            return int(inputs.get("Panel Count", 0)) * info["price_per_panel"]
        elif product == "Reflective Wrap":
            return sqft * info["price_per_sqft"]
        elif product == "Finish Options":
            return pricing.get(inputs.get("Finish", "Gloss"), 0.0)

    return 0.0

def calculate_quote(quote):
    business = quote["Business"]
    product = quote["Inputs"].get("Product", "")
    inputs = quote["Inputs"]
    base_cost = calculate_product_price(business, product, inputs)
    tax = round(base_cost * 0.07, 2)
    total = round(base_cost + tax, 2)

    quote["Outputs"]["Product"] = product
    quote["Outputs"]["Base Cost"] = round(base_cost, 2)
    quote["Outputs"]["Tax"] = tax
    quote["Outputs"]["Total Estimate"] = total

    return quote
