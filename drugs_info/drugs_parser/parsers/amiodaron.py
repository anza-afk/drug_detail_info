


url = 'https://www.lsgeotar.ru/amiodaron-18407.html'

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
options = Options()
options.add_argument("--headless")


def dict_from_drug_data(browser) -> dict:
    name = browser.find_element(By.CLASS_NAME, 'name-preparat-text').text
    try:
        description = browser.find_element(By.ID, 'sposob').find_element(
            By.CLASS_NAME, 'value').text.strip()
    except NoSuchElementException:
        description = ''
    try:
        recipe_only_data = browser.find_element(By.CLASS_NAME, 'ls-uslovia-otpuska').find_element(By.CLASS_NAME, 'value').text.strip()
        recipe_only = True if recipe_only_data.lower() != 'Без рецепта' else False
    except NoSuchElementException:
        recipe_only = None
    try:
        form_of_release = browser.find_element(By.ID, 'forma_vipuska').text.split(':')[1].strip()
    except IndexError:
        form_of_release = ''
    active_ingredient_data = browser.find_element(
        By.ID, 'sostav').text.split('компонент\n')
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
    return {
        'name': name,
        'description': description,
        'recipe_only': recipe_only,
        'form_of_release': form_of_release,
        'active_ingredient': active_ingredient
    }

with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
) as browser:
    print(dict_from_drug_data(browser))