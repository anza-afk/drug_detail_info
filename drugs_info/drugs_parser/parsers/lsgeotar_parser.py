
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument("--headless")


with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as browser:
    browser.implicitly_wait(2)
    browser.get('https://www.lsgeotar.ru/abc-pharma_tn/pg_000a2.html')

    abc_pages = browser.find_element(By.CLASS_NAME, 'abc_cyr').find_elements(By.TAG_NAME, 'a')
    abc_pages_hrefs = [page.get_attribute('href') for page in abc_pages]

    print(abc_pages_hrefs)

    current_letter_pages = browser.find_element(By.CLASS_NAME, 'wrap-abc-words').find_elements(By.TAG_NAME, 'a')
    pages_hrefs = [page.get_attribute('href') for page in current_letter_pages]

    print(pages_hrefs)

    links = browser.find_elements(By.CLASS_NAME, 'title-tn-link')[:1]
    current_page_hrefs = [link.get_attribute('href') for link in links]
    for href in current_page_hrefs:
        browser.get(href)
        name = browser.find_element(By.CLASS_NAME, 'name-preparat-text').text
        description = browser.find_element(By.ID, 'sposob').find_element(By.CLASS_NAME, 'value').text.strip()
        recipe_only_data = browser.find_element(By.CLASS_NAME, 'ls-uslovia-otpuska').text.split(':')[1].strip()
        recipe_only = True if recipe_only_data.lower() != 'Без рецепта' else False
        form_of_release = browser.find_element(By.ID, 'forma_vipuska').text.split(':')[1].strip()
        active_ingredient_data = browser.find_element(By.ID, 'sostav').text.split('компонент\n')
        active_ingredient = []
        for i in active_ingredient_data:
            for a in i.split('\n'):
                if any({'вспомогательные' in a.lower(), 'вспомогательное' in a.lower(), 'состав' in a.lower()}):
                    break
                if any({
                    'действующее' in a.lower(),
                    'действующие' in a.lower(),
                    'не содержит' in a.lower()
                }):
                    continue
                active_ingredient.append(a.strip().replace('.', '').replace(';', '').capitalize())
        print(f'{name}\nОТПУСК --- {form_of_release}\nВЕЩЕСТВА --- {active_ingredient}\nРЕЦЕПТ --- {recipe_only}\n<<<<<<<<<>>>>>>>>>{description}')
        browser.implicitly_wait(2)
