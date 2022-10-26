from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from rls_parser_methods import get_drug_info, get_drug_links, rls_authorization
from rls_parser_settings import URL, AUTH_DATA, AUTH_URL

options = Options()
options.add_argument("--headless")


with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
    ) as browser:
    rls_authorization(browser=browser, auth_url=AUTH_URL, auth_data=AUTH_DATA)
    browser.implicitly_wait(7)
    get_drug_links(browser=browser, url=URL)
