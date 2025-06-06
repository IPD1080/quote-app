from datetime import datetime

product_catalog = {
    "Independent Print": {
        ...  # Existing print products stay the same
    },
    "Independent Wraps": {
        ...  # Existing wrap products stay the same
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
            return info["pricing"].get(qty, 0.0) if isinstance(info["pricing"], dict) else 0.0
        elif "price_per_100" in info:
            return round((qty / 100) * info["price_per_100"], 2)
        elif product == "Stretched Canvas Prints" or product == "Acrylic Prints" or product == "Window Clings":
            size = inputs.get("Size", "")
            return info["pricing"].get(size, 0.0) * qty
        elif product == "Wall Decals":
            size = inputs.get("Size", "")
            return info["pricing"].get(size, 0.0)
        elif product == "Apparel":
            colors = int(inputs.get("Number of Colors", 1))
            area = inputs.get("Print Area", "Front")
            base = info["base_price_per_unit"]
            extra = (colors - 1) * info["extra_color_cost"]
            back = info["back_print_cost"] if area == "Both" else 0
            return round(qty * (base + extra + back), 2)

    elif business == "Independent Wraps":
        if product == "Partial Wrap":
            sqft = float(inputs.get("Sq Ft", 0))
            return round(sqft * info["base_price_per_sqft"], 2)
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
        elif product == "Reflective Wrap":
            sqft = float(inputs.get("Sq Ft", 0))
            return sqft * info["price_per_sqft"]
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
