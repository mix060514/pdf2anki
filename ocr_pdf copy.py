import os
from paddlex import create_pipeline
import fitz
from pdf2image import convert_from_path

# Create OCR pipeline
pipeline = create_pipeline(pipeline="OCR", device='gpu', model_type="ch_PP-OCRv4-server")

# Get all PDF files from splited_pdf folder
pdf_folder = "./splited_pdf"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Process each PDF file
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Process each page
    for i, image in enumerate(images):
        # Save image temporarily
        temp_image_path = f"temp_page_{i}.png"
        image.save(temp_image_path)
        
        # Perform OCR
        output = pipeline.predict(
            input=temp_image_path,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )
        
        # Save results
        output_base = os.path.join("output", pdf_file.replace(".pdf", ""))
        os.makedirs(output_base, exist_ok=True)
        
        for res in output:
            res.print()
            res.save_to_img(save_path=output_base)
            res.save_to_json(save_path=output_base)
        
        # Clean up temporary image
        os.remove(temp_image_path)
