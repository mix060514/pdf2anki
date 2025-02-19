#%%
import ollama
from prompt_router import prompt_router
from pyperclip import copy
import pandas as pd
import asyncio
import pickle
import pickle


filtered_df = pd.read_pickle('filtered_df.pkl')
text_group = filtered_df.query("word_group == 12")[['text','x','y','width','height','score']].to_json(orient='records', force_ascii=False)
# copy(text_group)

model = 'deepseek-r1:14b'
model = 'codestral:22b-v0.1-q3_K_M'
# response = ollama.chat(model=model, messages=[
#     {'role': 'system', 'content': prompt_router.get_prompt('word_analysis3')},
#     {'role': 'user', 'content': f"Process this OCR text and format as JSON: {text_group}"}
# ])
# print(text_group)


# print(response['message']['content'])

# %%
# for response in ollama.chat(
#     model=model,
#     messages=[
#         {'role': 'system', 'content': prompt_router.get_prompt('word_analysis3')},
#         {'role': 'user', 'content': f"Process this OCR text and format as JSON: {text_group}"}
#     ],
#     stream=True
# ):
#     print(response['message']['content'], end='', flush=True)

#%%

try:
    with open('result.pkl', 'rb') as f:
        result = pickle.load(f)
except Exception:
    result = {}

groups = filtered_df.word_group.unique()
for group in groups:
    if group in result:
        continue
    text_group = filtered_df.query(f"word_group == {group}")[['text','x','y','width','height','score']].to_json(orient='records', force_ascii=False)
    response = ollama.chat(model=model, messages=[
        {'role': 'system', 'content': prompt_router.get_prompt('word_analysis3')},
        {'role': 'user', 'content': f"Process this OCR text and format as JSON: {text_group}"}
    ])

    result[group] = {'source': text_group, 'result': response}
    print(response['message']['content'])

    with open('result.pkl', 'wb') as f:
        pickle.dump(result, f)



# %%
