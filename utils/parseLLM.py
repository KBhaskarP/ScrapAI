import os
import requests
import json
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def parse_with_llm(dom_chunks, parse_description, max_retries=3):
    """
    Parse DOM chunks using an LLM.

    Args:
        dom_chunks (list): List of DOM chunks to parse.
        parse_description (str): Description of parsing task.
        max_retries (int, optional): Maximum number of retries. Defaults to 3.

    Returns:
        str: Parsed results joined with newlines.
    """
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("GROQ_MODEL")
    client = Groq(api_key=GROQ_API_KEY)

    def generate_prompt(chunk, description):
        return f"""You are an expert content analyzer. Extract specific, relevant information from the following text:
        {chunk}
        Request: {description}
        Instructions:
        1. Extract only information directly related to the request.
        2. Ensure extracted information is contextually relevant and accurate.
        3. Provide only the extracted information without additional explanations.
        4. If no relevant information is found, return an empty string.
        5. Present the extracted information in a clear, concise format.

        Extracted information:"""

    results = []
    for i, chunk in enumerate(dom_chunks):
        for attempt in range(max_retries):
            try:
                prompt = generate_prompt(chunk, parse_description)
                
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You are an expert content analyzer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=os.getenv("Temperature"),
                    max_tokens=os.getenv("Max_tokens"),
                    timeout=os.getenv("Timeout") 
                )
                
                result = response.choices[0].message.content.strip()
                if result:
                    results.append(result)
                break
            except requests.exceptions.Timeout:
                st.warning(f"Request timed out for chunk {i+1}. Retrying...")
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed for chunk {i+1}: {str(e)}")
                break  # Don't retry on API errors
            except Exception as e:
                if attempt == max_retries - 1:
                    st.error(f"Failed to process chunk {i+1} after {max_retries} attempts: {str(e)}")
                else:
                    st.warning(f"Attempt {attempt + 1} for chunk {i+1} failed. Retrying...")
        
        return "\n\n".join(results)

  
