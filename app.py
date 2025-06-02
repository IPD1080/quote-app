import streamlit as st
from quote_engine import calculate_quote, create_base_quote
from utils import save_quote_to_csv, export_quote_to_pdf
from datetime import datetime

# Branding toggle
business = st.radio("Select Business", ["Independent Print", "Independent Wraps"])
st.title(f"{business} Quote Calculator")

# Create a new quote base
quote = create_base_quote(business)

# Input form
with st.form("quote_form"):
    st.subheader("Customer Details")
    quote["Inputs"]["Customer Name"] = st.text_input("Customer Name")
    quote["Inputs"]["Vehicle Type"] = st.text_input("Vehicle Type")
    quote["Inputs"]["Service Type"] = st.selectbox("Service Type", ["Full Wrap", "Partial Wrap", "Decals", "Print Product"])
    quote["Inputs"]["Square Footage"] = st.number_input("Square Footage", 0.0, 10000.0, 100.0)
    quote["Inputs"]["Install Hours"] = st.number_input("Install Hours", 0.0, 100.0, 8.0)
    quote["Inputs"]["Design Needed (Yes/No)"] = st.radio("Design Needed?", ["Yes", "No"])
    quote["Inputs"]["Rush Job (Yes/No)"] = st.radio("Rush Job?", ["Yes", "No"])
    quote["Inputs"]["Premium Vinyl (Yes/No)"] = st.radio("Premium Vinyl?", ["Yes", "No"])
    quote["Inputs"]["Complex Wrap (Yes/No)"] = st.radio("Complex Wrap?", ["Yes", "No"])
    quote["Inputs"]["Pickup or Delivery"] = st.selectbox("Pickup or Delivery", ["Pickup", "Delivery"])
    quote["Inputs"]["ZIP Code"] = st.text_input("ZIP Code")

    st.subheader("Add-ons")
    quote["Add-ons"]["Wrap Removal (Sq Ft)"] = st.number_input("Wrap Removal (Sq Ft)", 0.0, 1000.0, 0.0)
    quote["Add-ons"]["After-hours Install"] = st.checkbox("After-hours Install (+20%)")
    quote["Add-ons"]["On-site Install"] = st.checkbox("On-site Install ($50)")
    quote["Add-ons"]["Extra Proof Revisions"] = st.number_input("Extra Design Revisions", 0, 10, 0)
    quote["Add-ons"]["Out-of-town Mileage"] = st.number_input("Out-of-town Mileage", 0.0, 500.0, 0.0)

    submitted = st.form_submit_button("Calculate Quote")

if submitted:
    quote = calculate_quote(quote, business)
    st.subheader("Quote Breakdown")
    for key, value in quote["Outputs"].items():
        st.write(f"**{key}:** ${value}")

    # Save & export
    if st.button("💾 Save Quote"):
        save_quote_to_csv(quote)
        st.success("Quote saved to quotes.csv")

    if st.button("📄 Export as PDF"):
        filename = f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        export_quote_to_pdf(quote, filename)
        with open(filename, "rb") as f:
            st.download_button("Download PDF", f, file_name=filename)
