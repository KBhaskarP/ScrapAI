import re
from urllib.parse import urlparse, parse_qs, urljoin
import streamlit as st

def detect_and_generate_urls(base_url, total_pages):
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
            new_path = path.replace(f"{prefix}{number}", f"{prefix}{{}}")
            return [urljoin(base_url, new_path.format(i)) if i > 1 else base_url for i in range(1, total_pages + 1)]

    # Check query patterns
    for key in query_patterns:
        if key in query:
            query_copy = query.copy()
            return [
                urljoin(base_url, f"{path}?{key}={i}") if i > 1 
                else base_url for i in range(1, total_pages + 1)
            ]

    # If no pattern is found, assume the base_url is for all pages
    st.warning("No pagination pattern detected. Using the same URL for all pages.")
    return [base_url] * total_pages
