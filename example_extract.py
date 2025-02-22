from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from lib.prompt_router import prompt_router
from pydantic import BaseModel
from typing import List, Optional

# Define a simple model
class WordAnalysis(BaseModel):
    word: str
    split_to_root_or_affix: Optional[dict]
    meanings: List[dict]
    derivatives: List[dict]
    examples_sentence: List[dict]

# Sample OCR data
sample_data = [
    {"text": "alphabetic", "x": 100, "y": 100, "width": 50, "height": 20, "score": 0.99},
    {"text": "an/alphabet/ic", "x": 160, "y": 100, "width": 100, "height": 20, "score": 0.95},
    {"text": "adj.", "x": 50, "y": 130, "width": 30, "height": 20, "score": 0.98},
    {"text": "字母的", "x": 90, "y": 130, "width": 60, "height": 20, "score": 0.97},
    {"text": "The alphabetic system is easy to learn.", "x": 100, "y": 160, "width": 200, "height": 20, "score": 0.96},
    {"text": "字母系统很容易学。", "x": 100, "y": 190, "width": 150, "height": 20, "score": 0.95}
]

# Initialize components
parser = PydanticOutputParser(pydantic_object=WordAnalysis)
model = Ollama(
    model="deepseek-r1:8b",
    base_url="http://localhost:11434",
)

# Create prompt template
prompt = ChatPromptTemplate.from_template(prompt_router.get_prompt('word_analysis3'))

# Create chain
chain = prompt | model | parser

# Process sample data
import json
text_group = json.dumps(sample_data, ensure_ascii=False)
response = chain.invoke({"text_group": text_group})

# Print result
print("\nProcessed Result:")
print(response.model_dump_json(indent=2))
