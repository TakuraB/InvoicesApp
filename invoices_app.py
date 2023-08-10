import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to generate the invoice as a DataFrame
def generate_invoice(invoice_data):
    return pd.DataFrame(invoice_data)

# Function to display the invoice as text
def display_invoice(invoice_df):
    if len(invoice_df) == 0:
        st.warning("No items added to the invoice.")
        return
    
    st.subheader("Invoice Details:")
    st.text(f"Client Name: {invoice_df['Client Name'][0]}")
    st.text(f"Invoice Number: {invoice_df['Invoice Number'][0]}")
    st.text(f"Invoice Date: {invoice_df['Invoice Date'][0]}")
    st.text("Items:")
    for index, row in invoice_df.iterrows():
        st.text(f"  - {row['Item Description']}: ${row['Item Amount']:.2f}")
    st.subheader(f"Total: ${invoice_df['Item Amount'].sum():.2f}")

# Function to generate text invoice content
def generate_invoice_text(invoice_data):
    if len(invoice_data) == 0:
        return "No items added to the invoice."

    invoice_text = "Invoice Details:\n"
    for item in invoice_data:
        invoice_text += f"{item['Item Description']}: ${item['Item Amount']:.2f}\n"
    
    total_amount = sum(item['Item Amount'] for item in invoice_data)
    invoice_text += f"Total: ${total_amount:.2f}\n"
    
    return invoice_text
    if st.button("Download Invoice Text"):
        # Generate the text invoice using the session state data
        invoice_text = generate_invoice_text(st.session_state.invoice_data)
        
        # Display the invoice text
        st.subheader("Invoice Text:")
        st.text_area("Invoice Content", value=invoice_text, height=300)
        
        # Display a button to download the invoice text as a file
        st.download_button("Download Invoice Text", data=invoice_text.encode('utf-8'), file_name="invoice.txt")
# Function to generate and download text invoice
def download_invoice_as_text(invoice_data):
    if len(invoice_data) == 0:
        st.warning("No items added to the invoice.")
        return
    
    filename = "invoice.txt"
    with open(filename, 'w') as txt_file:
        txt_file.write("Invoice Details:\n")
        for item in invoice_data:
            txt_file.write(f"{item['Item Description']}: ${item['Item Amount']:.2f}\n")
        
        total_amount = sum(item['Item Amount'] for item in invoice_data)
        txt_file.write(f"Total: ${total_amount:.2f}\n")

    return filename  # Return the filename to use for the download link

# Main Streamlit application
def main():
    st.title("Invoice Generator")

    # Initialize invoice_data if not present in st.session_state
    if 'invoice_data' not in st.session_state:
        st.session_state.invoice_data = []

    # Collect user input
    client_name = st.text_input("Client Name", key="client_name")
    invoice_number = st.text_input("Invoice Number", key="invoice_number")
    invoice_date = st.date_input("Invoice Date", key="invoice_date")
    item_description = st.text_area("Item Description", key="item_description")
    item_amount = st.number_input("Item Amount", min_value=0.01, step=0.01, key="item_amount")

    if st.button("Add Item"):
        # Store invoice data in the session state
        st.session_state.invoice_data.append({
            "Client Name": client_name,
            "Invoice Number": invoice_number,
            "Invoice Date": invoice_date,
            "Item Description": item_description,
            "Item Amount": item_amount
        })

    if st.button("Generate Invoice"):
        # Create the invoice DataFrame
        invoice_df = generate_invoice(st.session_state.invoice_data)

        # Display the invoice
        display_invoice(invoice_df)

    if st.button("Download Invoice Text"):
        # Generate the text invoice using the session state data
        filename = download_invoice_as_text(st.session_state.invoice_data)
        
        # Display the download link for the text file
        st.download_button("Download Invoice Textfile", filename, key="download_button")


if __name__ == "__main__":
    main()
