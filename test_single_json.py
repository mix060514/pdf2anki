import json
from pathlib import Path

def process_single_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract and sort text by vertical position
    text_positions = []
    for poly, text in zip(data['dt_polys'], data['rec_text']):
        y_positions = [p[1] for p in poly]
        x_positions = [p[0] for p in poly]
        avg_y = sum(y_positions) / len(y_positions)
        min_x = min(x_positions)  # leftmost position
        text_positions.append({
            'text': text,
            'x_pos': min_x,
            'y_pos': avg_y
        })
    
    # Sort by y position
    sorted_texts = sorted(text_positions, key=lambda x: x['y_pos'])
    
    # Print results
    print("\nSorted texts by vertical position:")
    print("-" * 70)
    print(f"{'X':>8} | {'Y':>8} | Text")
    print("-" * 70)
    for item in sorted_texts:
        print(f"{item['x_pos']:8.2f} | {item['y_pos']:8.2f} | {item['text']}")

if __name__ == '__main__':
    # Replace this path with your JSON file path
    test_file = "./output/page_500/result_0.json"
    process_single_json(test_file)
