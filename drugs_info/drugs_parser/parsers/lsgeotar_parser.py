from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")


with webdriver.Chrome(options=options) as browser:
    browser.implicitly_wait(2)
    browser.get('https://www.lsgeotar.ru/abc-pharma_tn/pg_000a2.html')
    links = browser.find_elements(By.CLASS_NAME, 'title-tn-link')[:3]
    hrefs = [link.get_attribute('href') for link in links]
    for href in hrefs:
        browser.get(href)
        name = browser.find_element(By.CLASS_NAME, 'name-preparat-text').text
        minimal_age = ...
        recipe_only = ...
        form_of_release = ...
        active_ingredient = browser.find_element(By.ID, 'sostav').text.split(';')
        for i in active_ingredient:
            if any({'действующее' in i.lower(), 'действующие' in i.lower()}):
                print(name, i.split(':')[-1].strip().capitalize().split('\n'))
        browser.implicitly_wait(2)
