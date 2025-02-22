#%%
import pickle
import json
import csv

with open('result.pkl', 'rb') as f:
    raw_result = pickle.load(f) 

# More robust JSON string extraction
def extract_json_content(content):
    try:
        # Try direct JSON parsing first
        return json.loads(content)
    except:
        # Try finding JSON between code blocks
        try:
            json_blocks = content.split('```')
            for block in json_blocks:
                if block.strip().startswith(('json', '{')):
                    cleaned = block.replace('json', '').strip()
                    return json.loads(cleaned)
        except:
            pass
    return None

# Convert raw string result to dict 
result = {}
for key, value in raw_result.items():
    try:
        content = value['result']['message']['content']
        parsed_json = extract_json_content(content)
        
        if parsed_json:
            # Ensure we have a list of dictionaries, convert if needed
            if isinstance(parsed_json, dict):
                parsed_json = [parsed_json]
            elif not isinstance(parsed_json, list):
                parsed_json = []
                
            # Validate that all items are dictionaries
            if all(isinstance(item, dict) for item in parsed_json):
                result[key] = parsed_json
            else:
                print(f"Warning: Group {key} contains non-dictionary items")
                continue
                
    except Exception as e:
        print(f"Error processing group {key}: {str(e)}")

# Print stats about successfully parsed groups
valid_groups = list(result.keys())
print(f"Total valid groups: {len(valid_groups)}")
print(f"Valid groups: {sorted(valid_groups)}")

# Collect schema from all items
all_items = []
schema_keys = set()

for group in valid_groups:
    items = result[group]
    for item in items:
        schema_keys.update(item.keys())
        
# Standardize all items with complete schema
for group in valid_groups:
    items = result[group]
    for item in items:
        standardized_item = {key: item.get(key, None) for key in schema_keys}
        all_items.append(standardized_item)

print(f"Total items: {len(all_items)}")
print(f"Schema keys: {sorted(schema_keys)}")

# %%
print(result[15]['result']['message']['content'])
