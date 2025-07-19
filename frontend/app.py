import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Receipt and Bill Organizer")

st.header("Upload a new receipt")
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "pdf", "txt"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post("http://127.0.0.1:8001/upload/", files=files)
    if response.status_code == 200:
        st.success("Receipt uploaded and processed successfully!")
    else:
        st.error(f"Error uploading receipt: {response.text}")

st.header("Uploaded Receipts")
response = requests.get("http://127.0.0.1:8001/receipts/")
if response.status_code == 200:
    receipts = response.json()
    if receipts:
        df = pd.DataFrame(receipts)
        st.dataframe(df)

        st.header("Data Visualization")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Spending by Vendor")
            vendor_spending = df.groupby("vendor")["amount"].sum().reset_index()
            fig = px.pie(vendor_spending, values="amount", names="vendor", title="Spending by Vendor")
            st.plotly_chart(fig)

        with col2:
            st.subheader("Monthly Spending")
            df["transaction_date"] = pd.to_datetime(df["transaction_date"])
            df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
            monthly_spending = df.groupby("month")["amount"].sum().reset_index()
            fig = px.bar(monthly_spending, x="month", y="amount", title="Monthly Spending")
            st.plotly_chart(fig)

        st.header("Edit Receipt")
        receipt_to_edit = st.selectbox("Select a receipt to edit", df["id"])
        if receipt_to_edit:
            receipt_details = df[df["id"] == receipt_to_edit].iloc[0]
            with st.form(key="edit_form"):
                vendor = st.text_input("Vendor", value=receipt_details["vendor"])
                transaction_date = st.date_input("Transaction Date", value=pd.to_datetime(receipt_details["transaction_date"]))
                amount = st.number_input("Amount", value=receipt_details["amount"])
                category = st.text_input("Category", value=receipt_details["category"])
                submit_button = st.form_submit_button(label="Update Receipt")

                if submit_button:
                    updated_data = {
                        "vendor": vendor,
                        "transaction_date": transaction_date.isoformat(),
                        "amount": amount,
                        "category": category,
                    }
                    response = requests.put(f"http://127.0.0.1:8001/receipts/{receipt_to_edit}", json=updated_data)
                    if response.status_code == 200:
                        st.success("Receipt updated successfully!")
                    else:
                        st.error(f"Error updating receipt: {response.text}")

        st.header("Export Data")
        if st.button("Export to CSV"):
            df.to_csv("receipts.csv", index=False)
            st.success("Data exported to receipts.csv")

    else:
        st.info("No receipts found.")
else:
    st.error("Could not retrieve receipts.")
