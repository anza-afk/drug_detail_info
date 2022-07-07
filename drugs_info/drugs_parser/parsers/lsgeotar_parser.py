from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By


with webdriver.Chrome() as browser:
    browser.get('https://www.lsgeotar.ru/abc-pharma_tn/pg_000a2.html')
    links = browser.find_elements(By.CLASS_NAME, 'title-tn-link')
    for link in links:
        print('found', link)
        # link.click()
