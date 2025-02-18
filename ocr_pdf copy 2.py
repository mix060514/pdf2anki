import os
from paddlex import create_pipeline
import fitz
import json

# Create OCR pipeline
pipeline = create_pipeline(pipeline="OCR", device='gpu')

# Get all PDF files from splited_pdf folder
pdf_folder = "./splited_pdf"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Process each PDF file
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    
    # Open PDF with fitz
    pdf_document = fitz.open(pdf_path)
    
    # Process each page
    for i in range(len(pdf_document)):
        page = pdf_document.load_page(i)
        pix = page.get_pixmap()
        
        # Save image temporarily
        temp_image_path = f"temp_page_{i}.png"
        pix.save(temp_image_path)
        
        # Perform OCR
        output = pipeline.predict(
            input=temp_image_path
        )
        
        print(type(output))

        # Save results
        output_base = os.path.join("output", pdf_file.replace(".pdf", ""))
        os.makedirs(output_base, exist_ok=True)
        
        for res in output:
            res.print()
            res.save_to_img(save_path=output_base)
            json_path = os.path.join(output_base, f"result_{i}.json")
            with open(json_path, 'w', encoding='utf-8') as json_file:
                result_data = {
                    "input_path": res["input_path"],
                    "dt_polys": [_.tolist() for _ in res["dt_polys"]],  # list[ndarray, ndarray, ...]
                    "dt_scores": res["dt_scores"],  # list[float, float, ...]
                    "rec_text": res["rec_text"], # list[str, str, ...]
                    "rec_score": res["rec_score"], # list[float, float, ...]
                }
                json.dump(result_data, json_file, ensure_ascii=False, indent=4)
        
        # Clean up temporary image
        os.remove(temp_image_path)

