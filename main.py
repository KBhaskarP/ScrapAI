import streamlit as st
from utils.scrap import scrape_website_free
from utils.cleaner import split_dom_content, extract_content, clean_content
from utils.saveContent import save_html
from utils.parseLLM import parse_with_llm
from utils.body_analyzer import analyze_html
from utils.pagination import detect_and_generate_urls
from utils.notify import send_completion_email  # Import the function from notify.py

st.title("ScrapAI")

# Initialize session state variables
if 'last_scraped_url' not in st.session_state:
    st.session_state.last_scraped_url = ""
if 'url_changed' not in st.session_state:
    st.session_state.url_changed = True

# Function to update URL
def update_url():
    st.session_state.url_changed = st.session_state.current_url != st.session_state.last_scraped_url

# Function to handle scraping
def scrape_site():
    if st.session_state.url_changed:
        st.write("Please wait! We are working...")
        
        try:
            all_content = []
            BASE_URL = st.session_state.current_url
            total_pages = st.session_state.total_pages
            
            page_urls = detect_and_generate_urls(BASE_URL, total_pages)
            
            # Create placeholder for status
            status_placeholder = st.empty()
            
            for index, page_url in enumerate(page_urls):
                # Extract the actual page number from the URL
                actual_page_number = int(page_url.split('-')[-1].split('.')[0])
                
                # Update status message
                status_placeholder.write(f"Scraping page {index + 1} of {total_pages}: {page_url}")
                
                RESULT = scrape_website_free(page_url)
                BODY_CONTENT = extract_content(RESULT)
                CLEANED_CONTENT = clean_content(BODY_CONTENT)
                
                # Save and analyze immediately after scraping each page
                save_result = save_html(BODY_CONTENT, page_url, actual_page_number)
                html_analysis = analyze_html(page_url, actual_page_number)
                
                all_content.append({
                    "page": actual_page_number,
                    "page_url": page_url,
                    "body_content": BODY_CONTENT,
                    "cleaned_content": CLEANED_CONTENT
                })
            
            st.session_state.all_content = all_content
            st.session_state.current_page = 1
            st.session_state.analysis_completed = "All content saved and analyzed successfully!"

            # After successful scraping, update the last_scraped_url and set url_changed to False
            st.session_state.last_scraped_url = BASE_URL
            st.session_state.url_changed = False

            # Send completion email if enabled
            if st.session_state.send_email:
                if send_completion_email(BASE_URL, total_pages):
                    st.success("Completion email sent successfully!")
                else:
                    st.warning("Failed to send completion email.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Clear the status placeholder after completion
            status_placeholder.empty()

BASE_URL = st.text_input("Enter the URL of the first page (including any query parameters): ", 
                         key="current_url", on_change=update_url)

if BASE_URL:
    total_pages = st.number_input("Enter the number of pages to scrape:", min_value=1, value=1, step=1, key="total_pages")

    # Add email notification checkbox
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
            DOM_CHUNKS = split_dom_content(current_page_data["cleaned_content"])
            extracted_info = parse_with_llm(DOM_CHUNKS, PARSE_DESCRIPTION)
            st.text_area("Extracted Information:", extracted_info, height=100)
