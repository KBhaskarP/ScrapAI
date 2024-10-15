import os
import json
from datetime import datetime
from cleaner import remove_script_and_style_tags

def save_html(body_content,url):
    """
    Save the content of the body of an HTML page to a file.

    :param body_content: The content of the body of an HTML page.
    :return: The string "Content Saved".
    """
    body_content = remove_script_and_style_tags(body_content)
    current_time = datetime.now().strftime("%H_%M_%S_%f")
    segment = url_name_seggregation(url)
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(f"data/{segment}_content_{current_time}.html", 'w', encoding="utf-8") as f:
        f.write(body_content)
    return "Content Saved"

def url_name_seggregation(url):

    """
    This function takes a URL and returns the first segment of the URL.
    :param url: The URL to be processed.
    :return: The first segment of the URL.
    """
    
    url = url
    result = url.split("//")[1].split(".")[0]
    return result

def save_results_to_json(url, metadata, html_structure, keywords, lists, tables, links, folder='analysis_result'):
    
    """
    Save the results of HTML analysis to a JSON file.

    :param url: The URL of the webpage that was analyzed.
    :param metadata: A dictionary containing the title, meta description, and meta keywords of the webpage.
    :param html_structure: A dictionary containing the tag counts of the HTML structure.
    :param keywords: A list of the 10 most common words in the webpage, excluding stopwords.
    :param lists: A list of lists, where each sublist contains the text of the items in a list on the webpage.
    :param tables: A list of dictionaries, where each dictionary represents a table on the webpage, and contains the rows of the table as a list of dictionaries.
    :param links: A list of dictionaries, where each dictionary represents a link on the webpage, and contains the text and URL of the link.
    :param folder: The folder to save the results to. Defaults to "analysis_result".

    :return: The string "Analysis results saved to '{file_path}'."
    """
    url_name=url_name_seggregation(url)
    current_time = datetime.now().strftime("%H_%M_%S_%f")
    filename='html_analysis_results.json'
    # Create directory if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Path for the output JSON file
    file_path = os.path.join(folder, f"{url_name}_{current_time}_{filename}")

    results = {
        'metadata': metadata,
        'html_structure': html_structure,
        'keywords': keywords,
        'lists': lists,
        'tables': tables,
        'links': links
    }

    with open(file_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"Analysis results saved to '{file_path}'.")