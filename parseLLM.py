import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting **specific, relevant information** from the following text content: {dom_content}. "
    "Please follow these instructions with utmost precision:\n\n"
    "1. **Strict Matching:** Extract only the information that directly corresponds to the description provided: {parse_description}. "
    "Be precise in your extraction, and avoid including information that doesn't match the exact request.\n\n"
    "2. **Contextual Relevance:** Ensure that the extracted information aligns with the broader context of the description. "
    "If necessary, interpret the surrounding content to ensure the accuracy of the extraction.\n\n"
    "3. **No Extra Content:** Do not provide any explanations, commentary, or additional text. "
    "Your response should only contain the extracted information and nothing else.\n\n"
    "4. **Empty Response if No Match:** If no information directly matches the description, return an empty string (''). "
    "Avoid returning unrelated data or partial matches.\n\n"
    "5. **Well-Structured Data:** Provide the extracted information in a well-structured and concise format. "
    "If the extracted information contains multiple values, separate them clearly using commas or line breaks, depending on context.\n\n"
    "6. **Direct Output:** Your output should only contain the requested data in a clean format, without any extraneous symbols or characters."
)
load_dotenv()
MODEL = OllamaLLM(model=f"{os.getenv("MODEL_NAME")}")

def parse_with_llm(dom_chunks,parse_description):
    """
    Takes a list of dom chunks and a description of what to parse, and returns a string with the extracted information.

    :param dom_chunks: A list of strings where each string is a chunk of dom content.
    :param parse_description: A string that describes what information to extract from the dom content.
    :return: A string of the extracted information, with each extracted value on a new line.
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | MODEL
    parsed_results=[]
    for i , chunk in enumerate(dom_chunks,start=1) :
        response = chain.invoke({
            "dom_content":chunk,
            "parse_description":parse_description
        })
        print(f"batch {i} parsed of len {len(dom_chunks)}")
        parsed_results.append(response)
    return "\n".join(parsed_results)


    