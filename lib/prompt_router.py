import os
from pathlib import Path

class PromptRouter:
    def __init__(self):
        self.prompt_dir = Path(__file__).parent.parent / "prompts"
        self.cache = {}
        self.prompts = {
            'word_analysis3': '''You are a highly capable OCR analysis tool. Your task is to process an array of OCR data objects—each with text positions, content, and confidence scores—and produce a JSON response that exactly follows the structure below.

Input JSON Data: {text_group}

... rest of your prompt template ...
'''
        }

    def get_prompt(self, name: str) -> str:
        """
        Load a prompt by name from the prompts directory.
        The prompt file should be named {name}.txt
        """
        if name in self.cache:
            return self.cache[name]

        prompt_path = self.prompt_dir / f"{name}.txt"
        if not prompt_path.exists():
            raise ValueError(f"Prompt '{name}' not found at {prompt_path}")

        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
            self.cache[name] = prompt
            return prompt

# Create a global instance
prompt_router = PromptRouter()



