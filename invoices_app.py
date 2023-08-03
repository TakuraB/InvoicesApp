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

# Function to generate and download PDF invoice
def download_invoice_as_pdf(invoice_data):
    if len(invoice_data) == 0:
        st.warning("No items added to the invoice.")
        return
    
    filename = "invoice.pdf"
    pdf = canvas.Canvas(filename, pagesize=letter)

    pdf.drawString(100, 750, "Invoice Details:")
    y_position = 730
    for item in invoice_data:
        y_position -= 20
        pdf.drawString(120, y_position, f"{item['Item Description']}: ${item['Item Amount']:.2f}")
    
    total_amount = sum(item['Item Amount'] for item in invoice_data)
    pdf.drawString(120, y_position - 30, f"Total: ${total_amount:.2f}")
    pdf.save()

    st.success(f"Invoice PDF created and downloaded. Click [here](./{filename}) to download.")

# Main Streamlit application
def main():
    st.title("Invoice Generator")

    # Initialize invoice_data if not present in st.session_state
    if 'invoice_data' not in st.session_state:
        st.session_state.invoice_data = []

    # Flag to control the while loop
    generate_invoice_clicked = False

    while not generate_invoice_clicked:
        # Collect user input
        with st.form("invoice_form"):
            client_name = st.text_input("Client Name", key="client_name")
            invoice_number = st.text_input("Invoice Number", key="invoice_number")
            invoice_date = st.date_input("Invoice Date", key="invoice_date")
            item_description = st.text_area("Item Description", key="item_description")
            item_amount = st.number_input("Item Amount", min_value=0.01, step=0.01, key="item_amount")

            # Check if the "Add Item" button is clicked
            if st.form_submit_button("Add Item"):
                # Store invoice data in the session state
                st.session_state.invoice_data.append({
                    "Client Name": client_name,
                    "Invoice Number": invoice_number,
                    "Invoice Date": invoice_date,
                    "Item Description": item_description,
                    "Item Amount": item_amount
                })

        # Check if the "Generate Invoice" button is clicked
        if st.button("Generate Invoice"):
            # Set the flag to True to terminate the while loop
            generate_invoice_clicked = True

    # Create the invoice DataFrame
    invoice_df = generate_invoice(st.session_state.invoice_data)

    # Display the invoice
    display_invoice(invoice_df)

    if st.button("Download Invoice PDF"):
        # Generate and download the PDF invoice using the session state data
        download_invoice_as_pdf(st.session_state.invoice_data)

if __name__ == "__main__":
    main()
