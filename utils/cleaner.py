import re
from bs4 import BeautifulSoup

def extract_content(html_body):
    """
    Extract content from given html body string.

    :param html_body: The content of an HTML page in string format.
    :return: The extracted content in string format.
    """
    SOUP = BeautifulSoup(html_body, 'html.parser')
    CONTENT = SOUP.body
    if CONTENT:
        return str(CONTENT)
    return "Content is empty"


def clean_content(content):
    """
    Clean content by removing all the script and style tags from it.

    :param content: The content in string format.
    :return: The cleaned content in string format.
    """
    soup = BeautifulSoup(content, 'html.parser')
    for element in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
        element.decompose()
    
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def split_dom_content(dom_content, max_limit=6000):
    sentences = re.split(r'(?<=[.!?])\s+', dom_content)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_limit:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def remove_script_and_style_tags(content):
    """
    Remove all the script and style tags from the given content.

    :param content: The content in string format.
    :return: The cleaned content in string format.
    """
    soup = BeautifulSoup(content, 'html.parser')
    for script_soup in soup(["script", "style"]):
        script_soup.extract()
    return str(soup)
