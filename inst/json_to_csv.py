import os
import json
import csv
from pathlib import Path

def extract_text_positions(json_file):
    # Get page number from parent folder name by removing 'page_' prefix 
    page = int(json_file.parent.name.replace('page_', ''))
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    text_positions = []
    for poly, text, score in zip(data['dt_polys'], data['rec_text'], data['dt_scores']):
        # Calculate average x and y positions and width/height of the text box
        x_positions = [p[0] for p in poly]
        y_positions = [p[1] for p in poly]
        avg_x = sum(x_positions) / len(x_positions)
        avg_y = sum(y_positions) / len(y_positions)
        width = max(x_positions) - min(x_positions)
        height = max(y_positions) - min(y_positions)
        
        text_positions.append({
            'text': text,
            'x_pos': avg_x,
            'y_pos': avg_y,
            'width': width,
            'height': height,
            'score': score,
            'page': page
        })
    
    return sorted(text_positions, key=lambda x: x['y_pos'])

def concat_csv_files(csv_files, output_file):
    all_entries = []
    for csv_file in csv_files:
        with open(csv_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            all_entries.extend([[row[0], row[1], row[2], row[3], row[4], row[5], row[6]] for row in reader])
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Text', 'X', 'Y', 'Width', 'Height', 'Score', 'Page'])
        writer.writerows(all_entries)

def process_directory(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    csv_files = []  # Keep track of generated CSV files

    # Process each subdirectory (each PDF)
    for pdf_dir in input_path.iterdir():
        if pdf_dir.is_dir():
            pdf_texts = []
            
            # Process each JSON file in the PDF directory
            for json_file in pdf_dir.glob('*.json'):
                texts = extract_text_positions(json_file)
                pdf_texts.extend([[item['text'], item['x_pos'], item['y_pos'], 
                                 item['width'], item['height'], item['score'], item['page']] for item in texts])
            
            # Save to CSV
            csv_file = output_path / f"{pdf_dir.name}.csv"
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Text', 'X', 'Y', 'Width', 'Height', 'Score', 'Page'])
                writer.writerows(pdf_texts)
            csv_files.append(csv_file)
    
    # Concatenate all CSV files
    if csv_files:
        combined_output = 'combined_output.csv'
        concat_csv_files(csv_files, combined_output)
        print(f"Combined CSV saved to {combined_output}")

if __name__ == '__main__':
    process_directory('./output', './csv_output')
    print("Conversion completed. Check the csv_output directory.")
