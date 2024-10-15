import streamlit as st
from scrap import scrape_website_free
from cleaner import split_dom_content, extract_content, clean_content
from saveContent import save_html
from parseLLM import parse_with_llm
from body_analyzer import analyze_html

st.title("ScrapAI")
URL = st.text_input("Enter the URL: ")

if st.button("Scrape Site"):
    st.write("Please wait! We are working...")
    RESULT = scrape_website_free(URL)
    BODY_CONTENT = extract_content(RESULT)
    st.session_state.body_content = BODY_CONTENT
    CLEANED_CONTENT = clean_content(BODY_CONTENT)
    st.session_state.dom_content = CLEANED_CONTENT
    st.session_state.cleaned_content = CLEANED_CONTENT
    

if "body_content" in st.session_state:
    if st.button("Save Content"):
        result = save_html(st.session_state.body_content, URL)
        html_analysis = analyze_html(URL)
        
        # Store analysis result in session state
        st.session_state.analysis_completed = "Content saved and analyzed successfully!"

if "analysis_completed" in st.session_state and st.session_state.analysis_completed:
    st.success(st.session_state.analysis_completed)

if "cleaned_content" in st.session_state:
    with st.expander("Extracted Content"):
        st.text_area("DOM content:", st.session_state.cleaned_content, height=300, key="cleaned_content_area_repeat")

if "dom_content" in st.session_state:
    PARSE_DESCRIPTION = st.text_area("Describe what you want to find?")
    
    if st.button("Search"):
        if PARSE_DESCRIPTION:
            st.write("Parsing Content...")
            DOM_CHUNKS = split_dom_content(st.session_state.dom_content)
            extracted_info = parse_with_llm(DOM_CHUNKS, PARSE_DESCRIPTION)
            st.text_area("Extracted Information:", extracted_info, height=100)
