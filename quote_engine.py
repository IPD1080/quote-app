import streamlit as st
import pandas as pd
from quote_engine import create_base_quote, calculate_quote, product_catalog
from utils import save_quote_to_csv
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Quote Manager", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Quote Generator", "Quote History"])

# ------------------- QUOTE GENERATOR -------------------
if page == "Quote Generator":
    business = st.radio("Select Business", list(product_catalog.keys()))
    quote = create_base_quote(business)

    products = list(product_catalog[business].keys())
    product = st.selectbox("Select Product", products)
    quote["Inputs"]["Product"] = product

    if product in product_catalog[business]:
        st.subheader("Enter Product Details")
        inputs_required = product_catalog[business][product].get("inputs", [])

        for field in inputs_required:
            if "Qty" in field or "Quantity" in field:
                value = st.number_input(field, min_value=0, value=100, step=50)
            elif "Sq Ft" in field or "Area" in field:
                value = st.number_input(field, min_value=0.0, value=50.0)
            elif field == "Size":
                value = st.selectbox(field, ["2x4", "3x6", "4x8", "11x17", "18x24", "24x36", "4x6", "5x7", "8.5x11", "12x12", "16x20", "12x18", "36x48"])
            elif field == "Sides":
                value = st.selectbox(field, ["Single", "Double"])
            elif field in ["Grommets", "Hemming", "Laminate?"]:
                value = st.selectbox(field, ["Yes", "No"])
            elif field == "Coating":
                value = st.selectbox(field, ["None", "UV", "Gloss", "Matte"])
            elif field == "Paper Type":
                value = st.selectbox(field, ["Glossy", "Matte", "Uncoated"])
            elif field == "Shape":
                value = st.selectbox(field, ["Circle", "Square", "Custom"])
            elif field == "Finish":
                value = st.selectbox(field, ["Gloss", "Matte", "Satin", "Color Flip"])
            elif field == "Fold Type":
                value = st.selectbox(field, ["Tri-fold", "Bi-fold", "Z-fold"])
            elif field == "Binding":
                value = st.selectbox(field, ["Saddle Stitch", "Spiral", "Wire-O"])
            elif field == "Print Area":
                value = st.selectbox(field, ["Front", "Back", "Both"])
            elif field == "Complexity":
                value = st.selectbox(field, ["Normal", "Complex"])
            elif field == "Number of Colors":
                value = st.slider(field, 1, 6, 1)
            elif field in ["Color", "Font Type", "Material", "Item Type", "Vehicle Type", "Part", "Text Length", "Length", "Type", "Graphic Count", "Vehicle Count", "Panel Count"]:
                value = st.text_input(field)
            else:
                value = st.text_input(field)

            quote["Inputs"][field] = value

        quote["Inputs"]["Customer Name"] = st.text_input("Customer Name")
        quote["System"]["Business"] = business
        quote["System"]["Created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if st.button("Calculate Quote"):
            quote = calculate_quote(quote)
            st.subheader("Quote Summary")
            for k, v in quote["Outputs"].items():
                st.write(f"{k}: ${v}")

            if st.button("💾 Save Quote"):
                save_quote_to_csv(quote)
                st.success("Quote saved to quotes.csv")

# ------------------- QUOTE HISTORY -------------------
elif page == "Quote History":
    st.title("Quote History")
    path = Path("quotes.csv")
    if not path.exists():
        st.info("No quotes have been saved yet.")
    else:
        df = pd.read_csv(path)
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        with col1:
            business_filter = st.selectbox("Filter by Business", ["All"] + sorted(df["Business"].unique()))
        with col2:
            customer_filter = st.text_input("Filter by Customer Name")
        with col3:
            product_filter = st.selectbox("Filter by Product", ["All"] + sorted(df["Product"].unique()))

        filtered_df = df.copy()
        if business_filter != "All":
            filtered_df = filtered_df[filtered_df["Business"] == business_filter]
        if customer_filter:
            filtered_df = filtered_df[filtered_df["Customer Name"].str.contains(customer_filter, case=False, na=False)]
        if product_filter != "All":
            filtered_df = filtered_df[filtered_df["Product"] == product_filter]

        st.dataframe(filtered_df, use_container_width=True)

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Filtered Quotes", csv, "filtered_quotes.csv", "text/csv")
