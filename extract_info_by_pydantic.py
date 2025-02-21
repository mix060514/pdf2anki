from typing import Dict, List, Optional
from pydantic import BaseModel, Field
import ollama
from prompt_router import prompt_router
import pandas as pd
import pickle
from pathlib import Path
import json

class ExtractedInfo(BaseModel):
    """Base model for the structured information extracted by the LLM
    Note: This is just an example structure - modify according to your actual needs"""
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict] = None
    # Add other fields based on what information you expect the LLM to extract

class TextExtractor(BaseModel):
    model_name: str = Field(default="codestral:22b-v0.1-q3_K_M")
    result_path: Path = Field(default=Path("result3.pkl"))
    
    def load_results(self) -> Dict:
        """Load existing results from pickle file"""
        try:
            with open(self.result_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return {}

    def save_results(self, results: Dict) -> None:
        """Save results to pickle file"""
        with open(self.result_path, 'wb') as f:
            pickle.dump(results, f)

    def process_group(self, df: pd.DataFrame, group: int) -> ExtractedInfo:
        """Process a single group of text and return structured data"""
        text_group = (
            df.query(f"word_group == {group}")
            [['text', 'x', 'y', 'width', 'height', 'score']]
            .to_json(orient='records', force_ascii=False)
        )
        
        # You might want to modify the prompt to explicitly request JSON in the format
        # that matches your ExtractedInfo model
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    'role': 'system',
                    'content': prompt_router.get_prompt('word_analysis3')
                },
                {
                    'role': 'user',
                    'content': f"Process this OCR text and format as JSON: {text_group}"
                }
            ]
        )
        
        # Parse the LLM response and validate it with Pydantic
        try:
            llm_output = json.loads(response['message']['content'])
            return ExtractedInfo(**llm_output)
        except Exception as e:
            print(f"Error parsing LLM output for group {group}: {e}")
            return ExtractedInfo()  # Return empty structure if parsing fails

    def extract_all(self, df: pd.DataFrame) -> Dict[int, Dict]:
        """Extract information from all groups in the DataFrame"""
        results = self.load_results()
        groups = df.word_group.unique()
        
        for group in groups:
            if group in results:
                continue
                
            text_group = (
                df.query(f"word_group == {group}")
                [['text', 'x', 'y', 'width', 'height', 'score']]
                .to_json(orient='records', force_ascii=False)
            )
            
            extracted_info = self.process_group(df, group)
            
            results[group] = {
                'source': text_group,
                'result': extracted_info.model_dump()
            }
            
            print(f"Processed group {group}:", extracted_info)
            self.save_results(results)
            
        return results

def main():
    # Load the filtered DataFrame
    filtered_df = pd.read_pickle('filtered_df.pkl')
    
    # Initialize extractor
    extractor = TextExtractor()
    
    # Process all groups
    results = extractor.extract_all(filtered_df)
    
    return results

if __name__ == "__main__":
    main()
