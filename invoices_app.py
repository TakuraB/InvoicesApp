import streamlit as st
import pandas as pd

# Function to generate the invoice as a DataFrame
def generate_invoice(invoice_data):
    return pd.DataFrame(invoice_data)

# Main Streamlit application
def main():
    st.title("Invoice Generator")

    # Collect user input
    client_name = st.text_input("Client Name")
    invoice_number = st.text_input("Invoice Number")
    invoice_date = st.date_input("Invoice Date")
    item_description = st.text_area("Item Description")
    item_amount = st.number_input("Item Amount", min_value=0.01, step=0.01)

    if st.button("Add Item"):
        # Store invoice data in a list of dictionaries
        invoice_data.append({
            "Client Name": client_name,
            "Invoice Number": invoice_number,
            "Invoice Date": invoice_date,
            "Item Description": item_description,
            "Item Amount": item_amount
        })

    if st.button("Generate Invoice"):
        # Create the invoice DataFrame
        invoice_df = generate_invoice(invoice_data)

        # Display the invoice
        st.dataframe(invoice_df)

if __name__ == "__main__":
    # Initialize an empty list to store invoice data
    invoice_data = []
    main()
