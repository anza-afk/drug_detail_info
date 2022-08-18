from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
options = Options()
options.add_argument("--headless")

TEST_DATA = []


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


def get_current_page_hrefs(browser) -> list:
    current_letter_pages = browser.find_element(By.CLASS_NAME, 'wrap-abc-words').find_elements(By.TAG_NAME, 'a')
    return [page.get_attribute('href') for page in current_letter_pages]


def get_drug_links(browser) -> list:
    links = browser.find_elements(By.CLASS_NAME, 'title-tn-link')[:1]  # remove index here after test ^ ^
    return [link.get_attribute('href') for link in links]


def write_data(drug_dict: dict):
    with open('data.txt', 'a', encoding='utf8') as datafile:
        for key, value in drug_dict.items():
            datafile.writelines(f'{key}:{value}\n')
        datafile.writelines('\n')


def get_and_write_data_from_hrefs(browser):
    for href in current_page_hrefs:
        browser.get(href)
        data_dict = dict_from_drug_data(browser)
        write_data(data_dict)
    browser.implicitly_wait(2)


with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
) as browser:

    browser.implicitly_wait(2)
    browser.get('https://www.lsgeotar.ru/abc-pharma_tn/pg_000a2.html')
    current_page_hrefs = get_drug_links(browser)
    get_and_write_data_from_hrefs(browser)
    browser.back()
    a_hrefs = get_current_page_hrefs(browser)

    for page_href in a_hrefs:
        browser.get(page_href)
        current_page_hrefs = get_drug_links(browser)
        get_and_write_data_from_hrefs(browser)

    abc_pages = browser.find_element(By.CLASS_NAME, 'abc_cyr').find_elements(By.TAG_NAME, 'a')
    abc_pages_hrefs = [page.get_attribute('href') for page in abc_pages]

    for abc_href in abc_pages_hrefs:
        browser.get(abc_href)

        pages_hrefs = get_current_page_hrefs(browser)

        for page_href in pages_hrefs:
            browser.get(page_href)
            current_page_hrefs = get_drug_links(browser)
            get_and_write_data_from_hrefs(browser)
