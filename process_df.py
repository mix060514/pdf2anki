#%%
import pandas as pd

# Read the CSV file
df = pd.read_csv('combined_output.csv')
# Convert column names to lowercase
df.columns = df.columns.str.lower()
df = df.sort_values(['page','y']).reset_index(drop=True)
# Display the first few rows of the data
print(df.head())
# %%

df['is_word'] = df['text'].str.contains('[', regex=False) | df['text'].str.contains(']', regex=False)
df
# %%
df['word_group'] = df['is_word'].astype(int).cumsum()
df.iloc[20:].head(10)
# %%
filtered_df = df[df.groupby('word_group')['is_word'].transform('any')]
filtered_df.query("word_group == 3").head(15)
# %%
# Initialize Ollama with the deepseek model
import ollama

context = """The OCR data contains text positions and content. Each group includes English words, meanings, and example sentences.
Please analyze these entries and generate a JSON response with the following structure, and be aware that OCR results might contain errors that need human verification:
{
    // english
    "word": "English word",
    "split_to_root_or_affix": {
        // english, split by word 
        "value": "Root or affix",
        // english and chinese
        "meaning": "Root or affix meaning"
    },
    "meanings": [
        {
            // chinese
            "part_of_speech": "词性 (e.g., adj., n., v.)",
            // chinese
            "translation": "Chinese translation"
        }
    ],
    // optional, not every word has derivatives in book
    "derivatives": [ 
        "derivative word 1": {
            // chinese
            "part_of_speech": "词性 (e.g., adj., n., v.)",
            // chinese
            "translation": "Chinese translation"
        },
        "derivative word 2": {
            // chinese
            "part_of_speech": "词性 (e.g., adj., n., v.)",
            // chinese
            "translation": "Chinese translation"
        }    ],
    // optional, not every word has multiple derivatives in book, but at least one
    "examples_sentence": [
        {
            "english": "English example sentence (OCR result may need verification)",
            "chinese": "Chinese translation (OCR result may need verification)"
        }
    ]
}
example:

input:

'[{"text":"analphabetic [xnxlfobcttk]","x":90.0,"y":360.0,"width":136,"height":14,"score":0.7153835571},{"text":"an \\/alphabet \\/ic","x":116.0,"y":380.0,"width":80,"height":18,"score":0.78045706},{"text":"不字的","x":229.0,"y":387.0,"width":58,"height":14,"score":0.9358696295},{"text":"文盲","x":273.0,"y":387.0,"width":42,"height":14,"score":0.8854185376},{"text":"without\\/alphabet\\/形容字尾","x":124.0,"y":393.5,"width":128,"height":17,"score":0.9695865079},{"text":"• Fewer and fewer people are analphabetic nowadays.","x":153.5,"y":414.5,"width":241,"height":15,"score":0.959324793},{"text":"不留字的人如今愈来愈少見了","x":103.5,"y":429.5,"width":121,"height":13,"score":0.8009298725},{"text":"● My grandfather was an analphabetic all his life.","x":143.0,"y":449.0,"width":224,"height":18,"score":0.7906724306},{"text":"我能能终其一生是個文盲","x":94.0,"y":463.5,"width":104,"height":13,"score":0.9222601989}]'

output:
```json
{
    "word": "analphabetic",
    "split_to_root_or_affix": {
        "value": "an/alphabet/ic",
        "meaning": "without/alphabet/形容詞字尾"
    },
    "meanings": [
        {
            "part_of_speech": "形",
            "translation": "不識字的"
        },
        {
            "part_of_speech": "名",
            "translation": "文盲"
        }
    ],
    "derivatives": [],
    "examples_sentence": [
        {
            "english": "Fewer and fewer people are analphabetic nowadays.",
            "chinese": "不識字的人如越来越少見了。"
        },
        {
            "english": "My grandfather was an analphabetic all his life.",
            "chinese": "我爺爺終其一生是個文盲。"
        }
    ]
}
```
Please ensure all fields are properly formatted and maintain consistent structure."""

# text_group = filtered_df.query("word_group == 3")['text'].str.cat(sep='  \n  ')
text_group = filtered_df.query("word_group == 3")[['text','x','y','width','height','score']].to_json(orient='records', force_ascii=False)

response = ollama.chat(model='deepseek-r1:8b', messages=[
    {'role': 'system', 'content': context},
    {'role': 'user', 'content': f"Process this OCR text and format as JSON: {text_group}"}
])
print(text_group)


print(response['message']['content'])

# %%
