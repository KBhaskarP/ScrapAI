import re
from urllib.parse import urlparse, parse_qs, urljoin
import streamlit as st

def detect_pagination(url):
    """
    Detect if a given URL contains pagination elements.

    Args:
        url (str): The URL to check for pagination.

    Returns:
        bool: True if pagination is detected, False otherwise.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parse_qs(parsed_url.query)
    
    # Patterns to check
    path_patterns = [
        r'/page[/-]?\d+',
        r'/p[/-]?\d+',
        r'/\d+(?:\.html?)?$'
    ]
    query_patterns = ['page', 'p', 'pg', 'page_number']

    # Check path patterns
    for pattern in path_patterns:
        if re.search(pattern, path):
            return True

    # Check query patterns
    for key in query_patterns:
        if key in query:
            return True

    return False

def detect_and_generate_urls(base_url, total_pages):
    """
    Detect pagination pattern and generate URLs for multiple pages.

    Args:
        base_url (str): The initial URL to analyze.
        total_pages (int): Number of pages to generate URLs for.

    Returns:
        list: List of generated URLs for pagination.
    """
    parsed_url = urlparse(base_url)
    path = parsed_url.path
    query = parse_qs(parsed_url.query)
    
    # Patterns to check (in order of priority)
    path_patterns = [
        r'(/page[/-]?)(\d+)',
        r'(/p[/-]?)(\d+)',
        r'(/)(\d+)(?:\.html?)?$'
    ]
    query_patterns = ['page', 'p', 'pg', 'page_number']

    # Check path patterns
    for pattern in path_patterns:
        match = re.search(pattern, path)
        if match:
            prefix, number = match.groups()
            start_page = int(number)
            new_path = path.replace(f"{prefix}{number}", f"{prefix}{{}}")
            return [urljoin(parsed_url.scheme + "://" + parsed_url.netloc, new_path.format(i)) for i in range(start_page, start_page + total_pages)]

    # Check query patterns
    for key in query_patterns:
        if key in query:
            start_page = int(query[key][0])
            return [
                f"{parsed_url.scheme}://{parsed_url.netloc}{path}?{key}={i}" 
                for i in range(start_page, start_page + total_pages)
            ]

    # If no pattern is found, assume the base_url is for all pages
    st.warning("No pagination pattern detected. Using the same URL for all pages.")
    return [base_url] * total_pages
