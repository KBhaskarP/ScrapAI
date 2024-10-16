import os
import json
from datetime import datetime
from cleaner import remove_script_and_style_tags

def save_html(content, url, page_num):
    """
    Save the content of the body of an HTML page to a file.

    :param content: The content of the body of an HTML page.
    :param url: The URL of the webpage that was analyzed.
    :param page_num: The page number of the webpage that was analyzed.
    :return: The string "Content saved to '{file_path}'."
    """
    content = remove_script_and_style_tags(content)
    folder = 'data'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.now().strftime("%H_%M_%S_%f")
    filename = f'books_content_{timestamp}_{page_num}.html'
    file_path = os.path.join(folder, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return f"Content saved to {file_path}"

def url_name_seggregation(url):

    """
    This function takes a URL and returns the first segment of the URL.
    :param url: The URL to be processed.
    :return: The first segment of the URL.
    """
    
    url = url
    result = url.split("//")[1].split(".")[0]
    return result

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
    
    timestamp = datetime.now().strftime("%H_%M_%S_%f")
    filename = f'books_{timestamp}_{page_num}_html_analysis_results.json'
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