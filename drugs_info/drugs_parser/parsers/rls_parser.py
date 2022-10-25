from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
options = Options()
options.add_argument("--headless")
URL = 'https://www.rlsnet.ru/drugs/ukazatel'
with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
    ) as browser:
    browser.get(URL)
    abc_window = browser.find_element(
        By.CLASS_NAME, 'b-alphabet-body').find_element(By.CLASS_NAME, 'head')
    letters = [a.get_attribute('href') for a in abc_window.find_elements(By.TAG_NAME, 'a')]
    for a in letters:
        browser.get(a)
        with open('kirill-petooh.txt', 'a', encoding='UTF-8') as f:
            abc_list = browser.find_element(By.CLASS_NAME, 'b-alphabet-index')
            links = abc_list.find_elements(By.CLASS_NAME, 'link')
            for link in links:
                print('rere', link)
                for link in links:
                    f.writelines(f'{link.get_attribute("href")}\n')
