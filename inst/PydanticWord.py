#%%
from pydantic import BaseModel, Field


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
    think: str = Field(description="deepseek 思考過程")
    word: str = Field(description="Word")
    chinese_meaning: ChineseMeaning = Field(description="Chinese meaning with part of speech")
    word_root: WordRoot = Field(description="Word root")
    derived_words: list[DerivedWords] = Field(..., description="Derived words, which contains word, meaning, and part of speech")
    sentences: list[Sentence] = Field(description="Example sentences, can be one or two")
