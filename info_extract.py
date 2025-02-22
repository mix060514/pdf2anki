#%%
from langchain.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from lib.prompt_router import prompt_router
import pandas as pd
import pickle
from models.word_analysis import WordAnalysis

# Initialize parser and model
parser = PydanticOutputParser(pydantic_object=WordAnalysis)
model = Ollama(
    model="deepseek-r1:8b",
    base_url="http://localhost:11434",
)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_router.get_prompt('word_analysis3')),
    ("human", "Process this OCR text and format as JSON: {text_group}")
])

# Create chain
chain = prompt | model | parser

filtered_df = pd.read_pickle('filtered_df.pkl')




try:
    with open('result2.pkl', 'rb') as f:
        result = pickle.load(f)
except Exception:
    result = {}

groups = filtered_df.word_group.unique()
for group in groups:
    if group in result:
        continue
    
    text_group = filtered_df.query(f"word_group == {group}")[['text','x','y','width','height','score']].to_json(orient='records', force_ascii=False)
    
    # Process with LangChain
    response = chain.invoke({"text_group": text_group})
    
    result[group] = {'source': text_group, 'result': response.model_dump()}
    print(response.model_dump_json(indent=2))

    with open('result2.pkl', 'wb') as f:
        pickle.dump(result, f)

# %%
