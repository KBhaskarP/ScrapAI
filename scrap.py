import os
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv



load_dotenv()
# AUTH = f'{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}'
# SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

def scrape_website_free(website_url):
    print("Launching browser...")
    chrome_driver_path = f"{os.getenv("CHROMEDRIVER")}"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path),options=options)
    try:
        driver.get(website_url)
        html = driver.page_source
        return html
    finally:
        driver.quit()

# def scrape_website(website_url,sbr_webdriver=SBR_WEBDRIVER):

#     """
#     Use Selenium with BrightData to scrape a website that
#     includes a CAPTCHA. The function waits for the CAPTCHA to be
#     solved (or for 10 seconds to pass) and then returns the HTML of
#     the page.

#     :param website_url: The URL of the website to scrape
#     :param sbr_webdriver: The URL of the BrightData server. Defaults to
#         the value of the SBR_WEBDRIVER environment variable.

#     :return: The HTML content of the website after the CAPTCHA has been solved.

#     """
#     print("Launching browser...")
#     sbr_connection = ChromiumRemoteConnection(sbr_webdriver, 'goog', 'chrome')
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         driver.get(website_url)
#         html = driver.page_source
#         return html



