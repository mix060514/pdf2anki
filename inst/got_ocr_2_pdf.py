#%%
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
import fitz
import os
import json

import torch
from transformers import AutoProcessor, AutoModelForImageTextToText

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForImageTextToText.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf", device_map=device)
processor = AutoProcessor.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf")

# %%
from pathlib import Path

for img_file_path in Path("output3").rglob("*.png"):
    image_path = str(img_file_path)
    page_num = image_path.split("_")[-1].replace(".png", "")
    pdf_document = fitz.open(image_path)


    inputs = processor(image_path, return_tensors="pt").to(device)

    generate_ids = model.generate(
        **inputs,
        do_sample=False,
        tokenizer=processor.tokenizer,
        stop_strings="<|im_end|>",
        max_new_tokens=4096,
    )

    result = processor.decode(generate_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    print(result)

    output_base = Path("output44") / img_file_path.stem
    output_base.mkdir(parents=True, exist_ok=True)

    json_path = output_base / f"result_{page_num}.json"
    with open(json_path, 'w', encoding='utf-8') as json_file:
        result_data = {
            "result": result
        }
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)

