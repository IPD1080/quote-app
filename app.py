
import streamlit as st
from quote_engine import create_base_quote, calculate_quote, product_catalog

st.set_page_config(page_title="Quote Generator", layout="centered")

# Business selection
business = st.radio("Select Business", list(product_catalog.keys()))
quote = create_base_quote(business)

# Product selection
product = st.selectbox("Select Product", list(product_catalog[business].keys()))
quote["Inputs"]["Product"] = product

# Dynamic input fields based on product
st.subheader("Enter Product Details")
inputs_required = product_catalog[business][product]["inputs"]

for field in inputs_required:
    if "Qty" in field or "Quantity" in field:
        value = st.number_input(field, min_value=0, value=500, step=100)
    elif "Sq Ft" in field or "Area" in field:
        value = st.number_input(field, min_value=0.0, value=50.0)
    elif field in ["Laminate?", "Complexity"]:
        value = st.selectbox(field, ["Yes", "No"] if "Laminate" in field else ["Normal", "Complex"])
    else:
        value = st.text_input(field)
    quote["Inputs"][field] = value

if st.button("Calculate Quote"):
    quote = calculate_quote(quote)
    st.subheader("Quote Summary")
    for k, v in quote["Outputs"].items():
        st.write(f"{k}: ${v}")
