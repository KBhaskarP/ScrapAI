import os
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
    
    For example, if the URL is "https://techwithtim.net", the function will return "techwithtim".

    :param url: The URL to be processed.
    :return: The first segment of the URL.
    """
    
    url = "https://techwithtim.net"
    result = url.split("//")[1].split(".")[0]
    return result