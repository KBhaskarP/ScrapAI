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
    for script_soup in soup(["script", "style"]):
        script_soup.extract()
    cleanedContent = soup.get_text(separator="\n")
    cleanedContent = "\n".join(line.strip() for line in cleanedContent.splitlines() if line.strip())
    return cleanedContent

def split_dom_content(dom_content,max_limit=6000):
    """
    Split the given dom content into chunks of given max limit.

    :param dom_content: The content of a DOM in string format.
    :param max_limit: The maximum size of each chunk in bytes.
    :return: A list of strings, where each string is a chunk of the given content.
    """
    return [
        dom_content[i:i + max_limit] for i in range(0, len(dom_content), max_limit)
    ]

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