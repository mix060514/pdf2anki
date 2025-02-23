#%%
import fitz
import os

def pdf_to_images(pdf_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        name = pdf_path.split('_')[-1].replace('.pdf', '')
        print(f"{name=}")
        # Open PDF file
        doc = fitz.open(pdf_path)
        
        # Save only the first page as an image
        page = doc.load_page(0)  # Get first page

        # Increase resolution by applying a zoom matrix (2倍放大)
        zoom_factor = 20  # 可以调整为 2、3 或更高
        matrix = fitz.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=matrix)

        image_path = os.path.join(output_dir, f'image_{name}.png')
        pix.save(image_path)
        return True
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        return False

def main():
    # Example usage
    from pathlib import Path
    pdf_folder = Path("ref/splited_pdf")
    output_folder = "ref/splited_image"
    for pdf_file in pdf_folder.glob("*.pdf"):
        pdf_to_images(str(pdf_file), output_folder)

if __name__ == "__main__":
    main()
