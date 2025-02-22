#%% import pandas as pd
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

df0 = pd.read_csv('word_groups.csv')

#%%
class Sentence(BaseModel):
    eng: str = Field(description="English sentence")
    chi: str = Field(description="Chinese sentence")

class WordRoot(BaseModel):
    word_split: str = Field(description="Word split into parts")
    split_meaning: str = Field(description="Meaning of the split parts, can contains chinese description")

class ChineseMeaning(BaseModel):
    part_of_speech: str = Field(description="Part of speech")
    chinese_meaning: str = Field(description="Chinese meaning")

class DerivedWords(BaseModel):
    word: str = Field(description="Derived word")
    meaning: ChineseMeaning = Field(description="Meaning of the derived word")
    
class Word(BaseModel):
    think: str = Field(description="for the model to think in <think> tag")
    word: str = Field(description="Word")
    chinese_meaning: str = Field(description="Chinese meaning")
    word_root: WordRoot = Field(description="Word root")
    derived_words: list[DerivedWords] = Field(..., description="Derived words")
    sentences: list[Sentence] = Field(description="Example sentences, can be one or two")

# Initialize the model with structured output
llm = ChatOllama(model="deepseek-r1:8b", temperature=0)
structured_llm = llm.with_structured_output(Word, method="json_schema")

grp = 2
df_ = df0.query(f"word_group == {grp}")
df_
#%%
json_data = df_.to_dict('records')
json_data

#%%
prompt_text = f"""
the json input data is ocr result, which have x, y, text, page, chinese_text, english_text, is_word, is_chinese, is_english, english_length, chinese_length, is_chinese_sentence, is_english_sentence, word, word_group columns
i need you to extract the key information from this data
json_data: {json_data}

please be noticed that not all information is useful, you need to filter out the useful information
there is  a only main word in json_data, you need to know which part is for main word and which part is for derived words
and which is actually a next word but wrong to put here.

here is an example of the the structured, but format is wrong:
""" + """
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

pls <think> in <think> tag
"""
# result = structured_llm.invoke("Extract key information from this text: " + test_text, json_data=json_data)
result = structured_llm.invoke("Extract key information from this text: " + prompt_text)

print(result.think)
print(result.word)
print(result.chinese_meaning)
print(result.word_root)
print(result.derived_words)
print(result.sentences)

#%%

for grp in df0.word_group.unique():
    df_ = df0.query(f"word_group == {grp}")
    json_data = df_.to_dict('records')
    prompt_text = f"""
    the json input data is ocr result, which have x, y, text, page, chinese_text, english_text, is_word, is_chinese, is_english, english_length, chinese_length, is_chinese_sentence, is_english_sentence, word, word_group columns
    i need you to extract the key information from this data
    json_data: {json_data}

    please be noticed that not all information is useful, you need to filter out the useful information
    there is  a only main word in json_data, you need to know which part is for main word and which part is for derived words
    and which is actually a next word but wrong to put here.

    here is an example of the the structured, but format is wrong:
    """ + """
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

    pls <think> in <think> tag
    """
    # result = structured_llm.invoke("Extract key information from this text: " + test_text, json_data=json_data)
    result = structured_llm.invoke("Extract key information from this text: " + prompt_text)

    print(result.think)
    print(result.word)
    print(result.chinese_meaning)
    print(result.word_root)
    print(result.derived_words)
    print(result.sentences)
    if grp >= 5:
        break

# %%
