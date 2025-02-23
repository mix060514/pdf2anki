#%%
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

# Define a simple structured output model
class ExtractedContent(BaseModel):
    """Simple content extraction model"""
    think: str = Field(description="content in <think> tag")
    title: str = Field(description="The main title or heading")
    summary: str = Field(description="Brief summary of the content")
    key_points: list[str] = Field(description="List of key points")

# Initialize the model with structured output
llm = ChatOllama(model="deepseek-r1:8b", temperature=0)
structured_llm = llm.with_structured_output(ExtractedContent, method="json_schema")

# Example usage
test_text = """
Artificial Intelligence is transforming the world. It's being used in healthcare,
transportation, and education. Many companies are investing heavily in AI development.
"""

result = structured_llm.invoke("Extract key information from this text: " + test_text)
print(result.title)
print(result.summary)
print("\nKey Points:")
for point in result.key_points:
    print(f"- {point}")

# %%
result

# %%
