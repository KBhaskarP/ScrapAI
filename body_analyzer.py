from bs4 import BeautifulSoup
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from saveContent import save_results_to_json
import requests

# Download NLTK data (only need to do this once)
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

def analyze_html(url, page_num):
    """
    Analyze the HTML content of a webpage and extract metadata, HTML structure, keywords, lists, tables, and links.

    Parameters
    ----------
    url : str
        The URL of the webpage to analyze.

    Returns
    -------
    dict
        A dictionary containing the results of the analysis, with the following keys:

        * metadata: A dictionary containing the title, meta description, and meta keywords of the webpage.
        * html_structure: A dictionary containing the tag counts of the HTML structure.
        * keywords: A list of the 10 most common words in the webpage, excluding stopwords.
        * lists: A list of lists, where each sublist contains the text of the items in a list on the webpage.
        * tables: A list of dictionaries, where each dictionary represents a table on the webpage, and contains the rows of the table as a list of dictionaries.
        * links: A list of dictionaries, where each dictionary represents a link on the webpage, and contains the text and URL of the link.

    """
    response = requests.get(url,timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    
    metadata = {}
    metadata['title'] = soup.title.string if soup.title else 'No Title'
    
    meta_description = soup.find('meta', attrs={'name': 'description'})
    metadata['meta_description'] = meta_description['content'] if meta_description else 'No Meta Description'

    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    metadata['meta_keywords'] = meta_keywords['content'] if meta_keywords else 'No Meta Keywords'

    
    html_structure = {}
    tags = [tag.name for tag in soup.find_all()]
    tag_count = Counter(tags)
    html_structure['tag_counts'] = dict(tag_count)

    text = soup.get_text()
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    word_count = Counter(filtered_words)
    keywords = word_count.most_common(10)

    lists = []
    lists_data = soup.find_all(['ul', 'ol'])
    for lst in lists_data:
        list_items = [item.get_text() for item in lst.find_all('li')]
        lists.append(list_items)

    tables = []
    tables_data = soup.find_all('table')
    for table in tables_data:
        df = pd.read_html(str(table))[0]  # Read table into a DataFrame
        tables.append(df.to_dict(orient='records'))  # Convert DataFrame to dictionary

    links = []
    for a_tag in soup.find_all('a', href=True):
        link_info = {
            'text': a_tag.get_text(strip=True),
            'url': a_tag['href']
        }
        links.append(link_info)

    # Save results to JSON file
    return save_results_to_json(url, metadata, html_structure, keywords, lists, tables, links, page_num)
