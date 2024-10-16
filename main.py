import streamlit as st
from scrap import scrape_website_free
from cleaner import split_dom_content, extract_content, clean_content
from saveContent import save_html
from parseLLM import parse_with_llm
from body_analyzer import analyze_html
from pagination import detect_and_generate_urls

st.title("ScrapAI")

BASE_URL = st.text_input("Enter the URL of the first page (including any query parameters): ")
total_pages = st.number_input("Enter the number of pages to scrape:", min_value=1, value=1, step=1)

if st.button("Scrape and Save Site"):
    st.write("Please wait! We are working...")
    all_content = []
    
    page_urls = detect_and_generate_urls(BASE_URL, total_pages)
    
    # Create placeholders for dynamic content
    status_placeholder = st.empty()
    
    for page, page_url in enumerate(page_urls, start=1):
        # Update status message
        status_placeholder.write(f"Scraping page {page} of {total_pages}: {page_url}")
        
        RESULT = scrape_website_free(page_url)
        BODY_CONTENT = extract_content(RESULT)
        CLEANED_CONTENT = clean_content(BODY_CONTENT)
        
        # Save and analyze immediately after scraping each page
        save_result = save_html(BODY_CONTENT, page_url, page)
        html_analysis = analyze_html(page_url, page)
        
        all_content.append({
            "page": page,
            "page_url": page_url,
            "body_content": BODY_CONTENT,
            "cleaned_content": CLEANED_CONTENT
        })
    
    st.session_state.all_content = all_content
    st.session_state.current_page = 1
    st.session_state.analysis_completed = "All content saved and analyzed successfully!"

    # Clear the placeholders after completion
    status_placeholder.empty()

if "analysis_completed" in st.session_state and st.session_state.analysis_completed:
    st.success(st.session_state.analysis_completed)

if "all_content" in st.session_state:
    PARSE_DESCRIPTION = st.text_area("Describe what you want to find?")
    
    if st.button("Search"):
        if PARSE_DESCRIPTION:
            st.write("Parsing Content...")
            current_page_data = st.session_state.all_content[st.session_state.current_page - 1]
            DOM_CHUNKS = split_dom_content(current_page_data["cleaned_content"])
            extracted_info = parse_with_llm(DOM_CHUNKS, PARSE_DESCRIPTION)
            st.text_area("Extracted Information:", extracted_info, height=100)
