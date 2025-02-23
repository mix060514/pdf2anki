#%% 
import pandas as pd
from ollama import chat
from PydanticWord import Word, WordRoot, ChineseMeaning, DerivedWords, Sentence
# from pydantic import BaseModel
import json
import os
import pickle

tmp_file = 'word_groups_results.tmp'
final_file = 'word_groups_results.json'

try:
    with open(final_file, 'rb') as f:
        all_result = pickle.load(f)
except Exception as e:
    print(e)
    all_result = {}

#%%
# Initialize the model with structured output
model = "deepseek-r1:8b"
model = "deepseek-r1:7b"
model = "llama3.2"

df0 = pd.read_csv('word_groups.csv')
# df0.query("word_group == 61").to_dict('records')
for grp in df0.word_group.unique():
    if grp in all_result:
        continue
    df_ = df0.query(f"word_group == {grp}")
    # json_data = df_.to_dict('records')
    json_data = df_.to_markdown(index=False)
    prompt_text = """
You are provided with OCR output data from an English vocabulary book. Each entry in the JSON array contains the following keys:
- x, y, text, page, chinese_text, english_text, is_word, is_chinese, is_english, english_length, chinese_length, is_chinese_sentence, is_english_sentence, word, word_group

Your task is to extract the key information and output a valid JSON that meets the following requirements:

1. **Identify the Main Word and Related Entries:**
   - Determine which entry represents the main word (from the "word" field).
   - Separate out derived words and ignore any entries that represent a subsequent word mistakenly included.
   - consider the relation among the eng and chinese relation

2. **Revise and Correct OCR Errors:**
   - Many OCR results, especially for Chinese text, contain errors. Revise these as needed.
   - For the Chinese meaning, the expected format is a JSON object with keys "part_of_speech" and "chinese_meaning". For example:
     ```json
     {"part_of_speech": "名", "chinese_meaning": "祖先"}
     ```
   - If the OCR output merges these values (e.g., "名祖先前先"), split and correct them appropriately.
   - If the Chinese translation appears inaccurate, use your understanding of the word to provide a correct translation.
   
3. **Produce a Structured, Valid JSON Output:**
   Your final JSON should follow this structure:"""+ """
    {'$defs': {'ChineseMeaning': {'properties': {'part_of_speech': {'description': 'Part of speech',
 'title': 'Part Of Speech',
 'type': 'string'},
'chinese_meaning': {'description': 'Chinese meaning',
 'title': 'Chinese Meaning',
 'type': 'string'}},
'required': ['part_of_speech', 'chinese_meaning'],
'title': 'ChineseMeaning',
'type': 'object'},
'DerivedWords': {'properties': {'word': {'description': 'Derived word',
 'title': 'Word',
 'type': 'string'},
'meaning': {'$ref': '#/$defs/ChineseMeaning',
 'description': 'Meaning of the derived word'}},
'required': ['word', 'meaning'],
'title': 'DerivedWords',
'type': 'object'},
'Sentence': {'properties': {'eng': {'description': 'English sentence',
 'title': 'Eng',
 'type': 'string'},
'chi': {'description': 'Chinese sentence',
 'title': 'Chi',
 'type': 'string'}},
'required': ['eng', 'chi'],
'title': 'Sentence',
'type': 'object'},
'WordRoot': {'properties': {'word_split': {'description': 'Word split into parts',
 'title': 'Word Split',
 'type': 'string'},
'split_meaning': {'description': 'Meaning of the split parts, can contains chinese description',
 'title': 'Split Meaning',
 'type': 'string'}},
'required': ['word_split', 'split_meaning'],
'title': 'WordRoot',
'type': 'object'}},
'properties': {'think': {'description': 'deepseek 思考過程',
'title': 'Think',
'type': 'string'},
'word': {'description': 'Word', 'title': 'Word', 'type': 'string'},
'chinese_meaning': {'$ref': '#/$defs/ChineseMeaning',
'description': 'Chinese meaning with part of speech'},
'word_root': {'$ref': '#/$defs/WordRoot', 'description': 'Word root'},
'derived_words': {'description': 'Derived words, which contains word, meaning, and part of speech',
'items': {'$ref': '#/$defs/DerivedWords'},
'title': 'Derived Words',
'type': 'array'},
'sentences': {'description': 'Example sentences, can be one or two',
'items': {'$ref': '#/$defs/Sentence'},
'title': 'Sentences',
'type': 'array'}},
'required': ['think',
'word',
'chinese_meaning',
'word_root',
'derived_words',
'sentences'],
'title': 'Word',
'type': 'object'}

Ensure your output is valid JSON and includes all necessary corrections.

Context Note:
The OCR data is from an English word book, so use your best judgment to determine the correct Chinese translations and interpretations.
Finally, append the OCR data below after the label "json_data:".

Example Input :
    example json_data:
    [{'text': 'progenitor [pro°dynota)', 'x': 78.5, 'y': 236.5, 'width': 117, 'height': 17, 'score': 0.9201671018170704, 'page': 59, 'chinese_text': nan, 'english_text': 'progenitor [pro°dynota)', 'is_word': True, 'is_chinese': False, 'is_english': True, 'english_length': 23.0, 'chinese_length': 0.0, 'is_chinese_sentence': False, 'is_english_sentence': False, 'word': 'progenitor',
      'word_group': 61}, {'text': 'pro/gen/itor', 'x': 115.0, 'y': 255.5, 'width': 74, 'height': 17, 'score': 0.9204918776796308, 'page': 59, 'chinese_text': nan, 'english_text': 'pro/gen/itor', 'is_word': False, 'is_chinese': False, 'is_english': True, 'english_length': 12.0, 'chinese_length': 0.0, 'is_chinese_sentence': False, 'is_english_sentence': False,
      'word': 'pro/gen/itor', 'word_group': 61}, {'text': '祖先：前，先', 'x': 244.5, 'y': 256.0, 'width': 91, 'height': 14, 'score': 0.981616415040698, 'page': 59, 'chinese_text': '祖先前先', 'english_text': '：，', 'is_word': False, 'is_chinese': True, 'is_english': False, 'english_length': 6.0, 'chinese_length': 4.0, 'is_chinese_sentence': False,
      'is_english_sentence': False, 'word': '祖先：前，先', 'word_group': 61}, {'text': 'before/born/person', 'x': 115.5, 'y': 269.5, 'width': 95, 'height': 19, 'score': 0.8648172780564681, 'page': 59, 'chinese_text': nan, 'english_text': 'before/born/person', 'is_word': False, 'is_chinese': False, 'is_english': True, 'english_length': 18.0, 'chinese_length': 0.0,
      'is_chinese_sentence': False, 'is_english_sentence': False, 'word': 'before/born/person', 'word_group': 61}, {'text': 'progeny後代', 'x': 240.5, 'y': 271.5, 'width': 85, 'height': 17, 'score': 0.965889469427722, 'page': 59, 'chinese_text': '後代', 'english_text': 'progeny', 'is_word': False, 'is_chinese': True, 'is_english': True, 'english_length': 9.0,
      'chinese_length': 2.0, 'is_chinese_sentence': False, 'is_english_sentence': False, 'word': 'progeny後代', 'word_group': 61}, {'text': '■ Humans and monkeys share the same progenitor', 'x': 145.5, 'y': 291.5, 'width': 227, 'height': 13, 'score': 0.8455765307027225, 'page': 59, 'chinese_text': nan, 'english_text': '■ Humans and monkeys share the same progenitor', 'is_word': False, 'is_chinese': False, 'is_english': True,
      'english_length': 46.0, 'chinese_length': 0.0, 'is_chinese_sentence': False, 'is_english_sentence': True, 'word': '■ Humans and monkeys share the same progenitor', 'word_group': 61}, {'text': '人额與猴子有共同的祖先', 'x': 92.5, 'y': 306.0, 'width': 103, 'height': 10, 'score': 0.8134117296535087, 'page': 59, 'chinese_text': '人额與猴子有共同的祖先', 'english_text': nan, 'is_word': False, 'is_chinese': True,
      'is_english': False, 'english_length': 11.0, 'chinese_length': 11.0, 'is_chinese_sentence': True, 'is_english_sentence': False, 'word': '人额與猴子有共同的祖先', 'word_group': 61}, {'text': '● Sigmund Freud was the progenitor of modern psychology', 'x': 166.5, 'y': 327.5, 'width': 267, 'height': 13, 'score': 0.7956380989925946, 'page': 59, 'chinese_text': nan, 'english_text': '● Sigmund Freud was the progenitor of modern psychology', 'is_word': False,
      'is_chinese': False, 'is_english': True, 'english_length': 55.0, 'chinese_length': 0.0, 'is_chinese_sentence': False, 'is_english_sentence': True, 'word': '● Sigmund Freud was the progenitor of modern psychology', 'word_group': 61}, {'text': '西格蒙德·弗洛伊德是现代心理學的始祖', 'x': 123.0, 'y': 340.5, 'width': 162, 'height': 9, 'score': 0.913214570389693, 'page': 59, 'chinese_text': '西格蒙德弗洛伊德是现代心理學的始祖', 'english_text': '·',
      'is_word': False, 'is_chinese': True, 'is_english': False, 'english_length': 18.0, 'chinese_length': 17.0, 'is_chinese_sentence': True, 'is_english_sentence': False, 'word': '西格蒙德·弗洛伊德是现代心理學的始祖', 'word_group': 61}, {'text': 'prologue [pro,lg]', 'x': 67.0, 'y': 364.5, 'width': 94, 'height': 17, 'score': 0.878702832730834, 'page': 59, 'chinese_text': nan,
      'english_text': 'prologue [pro,lg]', 'is_word': True, 'is_chinese': False, 'is_english': True, 'english_length': 17.0, 'chinese_length': 0.0, 'is_chinese_sentence': False, 'is_english_sentence': False, 'word': 'prologue', 'word_group': 61}]

    sample result (need to be json and revise):
    {
     'word': 'progenitor',
     'chinese_meaning': {'part_of_speech': '名', 'chinese_meaning': '祖先'},
     'word_root': {'word_split': 'pro/gen/itor', 'split_meaning': '前世，先'},
     'derived_words': [],
     'sentences': [{'eng': "Progenitor is a term that refers to one's ancestors.",
       'chi': '祖先是指一个人的前代。'},
      {'eng': 'The progenitor of the technology industry is often considered to be someone like Tim Berners-Lee.',
       'chi': '科技产业的祖先通常被认为是蒂姆·伯恩斯-李等人。'}]}

    """   
    response = chat(
        messages=[
            {'role': 'system','content': "You are a very nice english teacher and very good at edit english book for chinese student.\n" + prompt_text},
            {'role': 'user',
             'content': "json_data: " + json_data
             },],
        model=model,
        format=Word.model_json_schema(),
    )
    # response
    print(response.message.content)

    # #%%
    all_result[grp] = response

    with open(tmp_file, 'wb') as f:
        pickle.dump(all_result, f)
    if os.path.exists(final_file):
        os.remove(final_file)
    os.rename(tmp_file, final_file)



# %%
