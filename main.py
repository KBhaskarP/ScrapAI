import streamlit as st
from utils.scrap import scrape_website_free
from utils.cleaner import split_dom_content, extract_content, clean_content
from utils.saveContent import save_html
from utils.parseLLM import parse_with_llm
from utils.body_analyzer import analyze_html
from utils.pagination import detect_pagination,detect_and_generate_urls
from utils.notify import send_completion_email
from utils.pdf_processor import process_pdf

st.title("ScrapAI")

# Initialize session state variables
if 'last_scraped_url' not in st.session_state:
    st.session_state.last_scraped_url = ""
if 'url_changed' not in st.session_state:
    st.session_state.url_changed = True
if 'is_paginated' not in st.session_state:
    st.session_state.is_paginated = False

# Function to update URL and check pagination
def update_url():
    st.session_state.url_changed = st.session_state.current_url != st.session_state.last_scraped_url
    st.session_state.is_paginated = detect_pagination(st.session_state.current_url)

# Function to handle scraping
def scrape_site():
    if st.session_state.url_changed:
        st.write("Please wait! We are working...")
        
        try:
            all_content = []
            BASE_URL = st.session_state.current_url
            
            # Create placeholder for status
            status_placeholder = st.empty()
            
            if st.session_state.is_paginated:
                total_pages = st.session_state.total_pages
                page_urls = detect_and_generate_urls(BASE_URL, total_pages)
                
                for index, page_url in enumerate(page_urls):
                    actual_page_number = index + 1
                    status_placeholder.write(f"Scraping page {actual_page_number} of {total_pages}: {page_url}")
                    
                    RESULT = scrape_website_free(page_url)
                    BODY_CONTENT = extract_content(RESULT)
                    CLEANED_CONTENT = clean_content(BODY_CONTENT)
                    
                    save_result = save_html(BODY_CONTENT, page_url, actual_page_number)
                    html_analysis = analyze_html(page_url, actual_page_number)
                    
                    all_content.append({
                        "page": actual_page_number,
                        "page_url": page_url,
                        "body_content": BODY_CONTENT,
                        "cleaned_content": CLEANED_CONTENT
                    })
            else:
                status_placeholder.write(f"Scraping single page: {BASE_URL}")
                
                RESULT = scrape_website_free(BASE_URL)
                BODY_CONTENT = extract_content(RESULT)
                CLEANED_CONTENT = clean_content(BODY_CONTENT)
                
                save_result = save_html(BODY_CONTENT, BASE_URL, 1)
                html_analysis = analyze_html(BASE_URL, 1)
                
                all_content.append({
                    "page": 1,
                    "page_url": BASE_URL,
                    "body_content": BODY_CONTENT,
                    "cleaned_content": CLEANED_CONTENT
                })
            
            st.session_state.all_content = all_content
            st.session_state.current_page = 1
            st.session_state.analysis_completed = "All content saved and analyzed successfully!"

            st.session_state.last_scraped_url = BASE_URL
            st.session_state.url_changed = False

            if st.session_state.send_email:
                if send_completion_email(BASE_URL, len(all_content)):
                    st.success("Completion email sent successfully!")
                else:
                    st.warning("Failed to send completion email.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            status_placeholder.empty()

BASE_URL = st.text_input("Enter the URL of the first page (including any query parameters): ", 
                         key="current_url", on_change=update_url)

st.subheader("Or upload a PDF file")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("PDF file uploaded successfully!")
    
    if st.button("Process PDF"):
        st.write("Processing PDF... Please wait.")
        pdf_content = process_pdf(uploaded_file)
        
        # Clean the extracted PDF content
        cleaned_pdf_content = clean_content(pdf_content)
        
        # Split the content into chunks
        pdf_chunks = split_dom_content(cleaned_pdf_content)
        
        # Store the PDF content in session state
        st.session_state.pdf_content = {
            "page": 1,
            "page_url": "Uploaded PDF",
            "body_content": pdf_content,
            "cleaned_content": cleaned_pdf_content
        }
        st.session_state.all_content = [st.session_state.pdf_content]
        st.session_state.current_page = 1
        st.session_state.analysis_completed = "PDF processed successfully!"
        
        st.success("PDF processed and ready for analysis!")

if BASE_URL:
    if st.session_state.is_paginated:
        total_pages = st.number_input("Enter the number of pages to scrape:", min_value=1, value=1, step=1, key="total_pages")
    
    st.session_state.send_email = st.checkbox("Send completion email", value=False)

    st.button("Scrape and Save Site", on_click=scrape_site, disabled=not st.session_state.url_changed)

if "analysis_completed" in st.session_state and st.session_state.analysis_completed:
    st.success(st.session_state.analysis_completed)

if "all_content" in st.session_state:
    PARSE_DESCRIPTION = st.text_area("Describe what you want to find?")
    
    if st.button("Search"):
        if PARSE_DESCRIPTION:
            st.write("Parsing Content...")
            current_page_data = st.session_state.all_content[st.session_state.current_page - 1]
            
            if current_page_data["page_url"] == "Uploaded PDF":
                DOM_CHUNKS = split_dom_content(current_page_data["cleaned_content"])
            else:
                DOM_CHUNKS = split_dom_content(current_page_data["cleaned_content"])
            
            extracted_info = parse_with_llm(DOM_CHUNKS, PARSE_DESCRIPTION)
            st.text_area("Extracted Information:", extracted_info, height=300)
