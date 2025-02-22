from pydantic import BaseModel
from typing import List, Optional

class SplitToRootOrAffix(BaseModel):
    value: str
    meaning: str

class Meaning(BaseModel):
    part_of_speech: str
    translation: str

class Derivative(BaseModel):
    word: str
    part_of_speech: str
    translation: str

class ExampleSentence(BaseModel):
    english: str
    chinese: str

class WordAnalysis(BaseModel):
    word: str
    split_to_root_or_affix: SplitToRootOrAffix
    meanings: List[Meaning]
    derivatives: List[Derivative]
    examples_sentence: List[ExampleSentence]
