
from datetime import datetime

def create_base_quote(business='Independent Print'):
    # Define pricing per business side
    if business == 'Independent Print':
        pricing = {
            "Labor Rate": 60,
            "Standard Vinyl Cost": 3.5,
            "Premium Vinyl Cost": 5.0,
            "Lamination Cost per Sq Ft": 1.0,
            "Rush Fee %": 20,
            "Complex Wrap Fee %": 0,
            "Design Flat Fee": 75,
            "Extra Design Hourly Fee": 50,
            "Old Wrap Removal Cost per Sq Ft": 0,
            "Travel/Delivery Fee": 25,
            "Out-of-town Mileage Rate": 0.5,
            "On-site Install Fee": 25,
            "Tax Rate %": 7,
        }
    else:
        pricing = {
            "Labor Rate": 75,
            "Standard Vinyl Cost": 3.5,
            "Premium Vinyl Cost": 5.0,
            "Lamination Cost per Sq Ft": 1.0,
            "Rush Fee %": 25,
            "Complex Wrap Fee %": 10,
            "Design Flat Fee": 150,
            "Extra Design Hourly Fee": 75,
            "Old Wrap Removal Cost per Sq Ft": 2.5,
            "Travel/Delivery Fee": 75,
            "Out-of-town Mileage Rate": 0.75,
            "On-site Install Fee": 50,
            "Tax Rate %": 7,
        }

    return {
        "Inputs": {
            "Customer Name": "",
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Vehicle Type": "",
            "Service Type": "",
            "Square Footage": 0,
            "Install Hours": 0,
            "Design Needed (Yes/No)": "No",
            "Rush Job (Yes/No)": "No",
            "Premium Vinyl (Yes/No)": "No",
            "Complex Wrap (Yes/No)": "No",
            "Pickup or Delivery": "Pickup",
            "ZIP Code": ""
        },
        "Pricing": pricing,
        "Add-ons": {
            "Wrap Removal (Sq Ft)": 0,
            "After-hours Install": False,
            "On-site Install": False,
            "Extra Proof Revisions": 0,
            "Out-of-town Mileage": 0
        },
        "Outputs": {
            "Material Cost": 0.0,
            "Labor Cost": 0.0,
            "Design Fee": 0.0,
            "Add-ons Total": 0.0,
            "Subtotal": 0.0,
            "Tax": 0.0,
            "Total Estimate": 0.0
        },
        "System": {
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": "Draft"
        }
    }

def calculate_quote(quote, business='Independent Print'):
    inputs = quote["Inputs"]
    pricing = quote["Pricing"]
    add_ons = quote["Add-ons"]
    outputs = quote["Outputs"]

    sqft = float(inputs["Square Footage"])
    install_hours = float(inputs["Install Hours"])

    # Material Cost
    vinyl_cost = pricing["Premium Vinyl Cost"] if inputs["Premium Vinyl (Yes/No)"] == "Yes" else pricing["Standard Vinyl Cost"]
    lamination_cost = pricing["Lamination Cost per Sq Ft"]
    outputs["Material Cost"] = round(sqft * (vinyl_cost + lamination_cost), 2)

    # Labor Cost
    labor_cost = install_hours * pricing["Labor Rate"]
    if add_ons["After-hours Install"]:
        labor_cost *= 1.2
    outputs["Labor Cost"] = round(labor_cost, 2)

    # Design Fee
    design_fee = 0
    if inputs["Design Needed (Yes/No)"] == "Yes":
        design_fee += pricing["Design Flat Fee"]
        design_fee += add_ons["Extra Proof Revisions"] * pricing["Extra Design Hourly Fee"]
    outputs["Design Fee"] = round(design_fee, 2)

    # Add-ons
    addons_total = 0
    addons_total += add_ons["Wrap Removal (Sq Ft)"] * pricing.get("Old Wrap Removal Cost per Sq Ft", 0)
    if inputs["Pickup or Delivery"] == "Delivery":
        addons_total += pricing["Travel/Delivery Fee"]
    if add_ons["On-site Install"]:
        addons_total += pricing["On-site Install Fee"]
    if add_ons["Out-of-town Mileage"] > 0:
        addons_total += add_ons["Out-of-town Mileage"] * pricing["Out-of-town Mileage Rate"]
    outputs["Add-ons Total"] = round(addons_total, 2)

    # Subtotal
    subtotal = outputs["Material Cost"] + outputs["Labor Cost"] + outputs["Design Fee"] + outputs["Add-ons Total"]
    if inputs["Rush Job (Yes/No)"] == "Yes":
        subtotal *= 1 + (pricing["Rush Fee %"] / 100)
    if inputs["Complex Wrap (Yes/No)"] == "Yes":
        subtotal *= 1 + (pricing["Complex Wrap Fee %"] / 100)
    outputs["Subtotal"] = round(subtotal, 2)

    # Tax and Total
    tax = subtotal * (pricing["Tax Rate %"] / 100)
    outputs["Tax"] = round(tax, 2)
    outputs["Total Estimate"] = round(subtotal + tax, 2)

    return quote
