import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, output_folder='splited_pdf'):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the PDF
    with open(input_path, 'rb') as file:
        pdf = PdfReader(file)
        
        # Split each page
        for page_num in range(len(pdf.pages)):
            # Create PDF writer object
            pdf_writer = PdfWriter()
            
            # Add page to writer
            pdf_writer.add_page(pdf.pages[page_num])
            
            # Create output filename
            output_filename = f'page_{page_num + 1}.pdf'
            output_path = os.path.join(output_folder, output_filename)
            
            # Write the page to a file
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)

if __name__ == "__main__":
    # Example usage
    input_pdf = "english_word.pdf"  # Replace with your PDF file path
    split_pdf(input_pdf)
    print("PDF splitting completed!")
