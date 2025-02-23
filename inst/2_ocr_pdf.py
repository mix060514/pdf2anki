#%%
import os
from paddlex import create_pipeline
import fitz
import json

from paddlex import create_model


# Create OCR pipeline
pipeline = create_pipeline(pipeline="OCR", device='gpu')

# Get all PDF files from splited_pdf folder
image_folder = "./ref/splited_image"
png_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

# Process each PDF file
for image_file in png_files:
    page_num = image_file.split('_')[-1].replace('.png', '')
    png_path = os.path.join(image_folder, image_file)
    
    # Load PNG image path directly
    image_path = png_path
    output = pipeline.predict( input=png_path)
    

    # Save results
    output_base = os.path.join("ref/ocr_result_json", image_file.replace(".png", ""))
    os.makedirs(output_base, exist_ok=True)
    
    for res in output:
        res.print()
        res.save_to_img(save_path=output_base)
        json_path = os.path.join(output_base, f"result_{page_num}.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            # print(res.keys())
            result_data = {
                "input_path": res["input_path"],
                "dt_polys": [_.tolist() for _ in res["dt_polys"]],  # list[ndarray, ndarray, ...]
                "dt_scores": res["dt_scores"],  # list[float, float, ...]
                "rec_text": res["rec_text"], # list[str, str, ...]
                "rec_score": res["rec_score"], # list[float, float, ...]
            }
            json.dump(result_data, json_file, ensure_ascii=False, indent=4)
        


# %%
