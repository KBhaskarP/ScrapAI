import streamlit as st
from scrap import scrape_website_free
from cleaner import split_dom_content,extract_content,clean_content
from saveContent import save_html
from parseLLM import parse_with_llm
# from parseLLM import parse_with_llm

st.title("ScrapAI")
URL = st.text_input("Enter the URL: ")
if st.button("Scrape Site"):
    st.write("Please wait! we are working...")
    RESULT=scrape_website_free(URL)
    BODY_CONTENT=extract_content(RESULT)
    st.session_state.body_content = BODY_CONTENT
    CLEANED_CONTENT=clean_content(BODY_CONTENT)
    st.session_state.dom_content=CLEANED_CONTENT
    with st.expander("Extracted Content"):
        st.text_area(f"DOM content: {CLEANED_CONTENT}",height=300)
    if st.button("Analyze HTML Content"):
        st.write("started")
if "body_content" in st.session_state:
    if st.button("Save Content"):
        result = save_html(st.session_state.body_content, URL)
        st.write(result)
if "dom_content" in st.session_state:
    PARSE_DESCRIPTION = st.text_area("Describe what you want to find?")
    if st.button("Search"):
        if PARSE_DESCRIPTION:
            st.write("Parsing Content...")
            DOM_CHUNKS = split_dom_content(st.session_state.dom_content)
            extracted_info = parse_with_llm(DOM_CHUNKS, PARSE_DESCRIPTION)
            st.text_area("Extracted Information:", extracted_info, height=300)
