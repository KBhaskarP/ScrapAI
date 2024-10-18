import os
import json
from datetime import datetime
from utils.cleaner import remove_script_and_style_tags
from urllib.parse import urlparse

def save_html(content, url, page_num):
    """
    Save the content of the body of an HTML page to a file.

    :param content: The content of the body of an HTML page.
    :param url: The URL of the webpage that was analyzed.
    :param page_num: The page number of the webpage that was analyzed.
    :return: The string "Content saved to '{file_path}'."
    """
    content = remove_script_and_style_tags(content)
    URL = url_name_segregation(url)
    folder = 'data'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.now().strftime("%H_%M_%S_%f")
    filename = f'{URL}_{timestamp}_{page_num}.html'
    file_path = os.path.join(folder, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return f"Content saved to {file_path}"

def url_name_segregation(url):
    """
    This function takes a URL and returns the domain name without the TLD.
    :param url: The URL to be processed.
    :return: The domain name without the TLD.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Split the domain and remove the TLD (e.g., .com, .org)
    domain_parts = domain.split('.')
    if len(domain_parts) > 2:
        return domain_parts[-2]
    elif len(domain_parts) == 2:
        return domain_parts[0]
    else:
        return domain

def save_results_to_json(url, metadata, html_structure, keywords, lists, tables, links, page_num):
    """
    Save the results of HTML analysis to a JSON file.

    :param url: The URL of the webpage that was analyzed.
    :param metadata: A dictionary containing the title, meta description, and meta keywords of the webpage.
    :param html_structure: A dictionary containing the tag counts of the HTML structure.
    :param keywords: A list of the 10 most common words in the webpage, excluding stopwords.
    :param lists: A list of lists, where each sublist contains the text of the items in a list on the webpage.
    :param tables: A list of dictionaries, where each dictionary represents a table on the webpage, and contains the rows of the table as a list of dictionaries.
    :param links: A list of dictionaries, where each dictionary represents a link on the webpage, and contains the text and URL of the link.
    :param page_num: The page number of the webpage that was analyzed.
    :return: The string "Analysis results saved to '{file_path}'."
    """
    folder = 'analysis_result'
    if not os.path.exists(folder):
        os.makedirs(folder)
    URL=url_name_segregation(url)
    timestamp = datetime.now().strftime("%H_%M_%S_%f")
    filename = f'{URL}_{timestamp}_{page_num}_html_analysis_results.json'
    file_path = os.path.join(folder, filename)
    
    results = {
        "url": url,
        "metadata": metadata,
        "html_structure": html_structure,
        "keywords": keywords,
        "lists": lists,
        "tables": tables,
        "links": links
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    
    return f"Analysis results saved to '{file_path}'."
