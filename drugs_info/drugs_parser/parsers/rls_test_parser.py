from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from rls_parser_methods import get_drug_info, get_drug_links, rls_authorization
from rls_parser_settings import URL, AUTH_DATA, AUTH_URL
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(sys.path[0], '../../'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drugs_info.drugs_info.settings")

import django
django.setup()

from drugs_api.models import DrugLink, Drug

options = Options()
options.add_argument("--headless")


def get_drug_info(browser, drug_url):
    drug_dict = {
        'name': None,
        'active_ingredient': [],
        'pharmacological_class': None,
        'form_of_release': None,
        'recipe_only': None,
    }
    browser.get(drug_url)
    slist = browser.find_element(By.CLASS_NAME, 'structure-list')
    drug_dict['name'] = browser.find_element(By.CLASS_NAME, 'heading').text
    if 'Действующее вещество' in slist.text:
        drug_dict['active_ingredient'].append(browser.find_element(
            By.XPATH, "//h2[@id='deistvuyushhee-veshhestvo']/following-sibling::div").text)
    if 'Фармакологическая группа' in slist.text:
        drug_dict['pharmacological_class'] = browser.find_element(
            By.XPATH, "//h2[@id='farmakologiceskaya-gruppa']/following-sibling::div").text
    if 'Форма выпуска' in slist.text:
        drug_dict['form_of_release'] = browser.find_element(
            By.XPATH, "//h2[@id='forma-vypuska']/following-sibling::div").text
    if 'Условия отпуска из аптек' in slist.text:
        drug_dict['recipe_only'] = browser.find_element(
            By.XPATH, "//h2[@id='usloviya-otpuska-iz-aptek']/following-sibling::div").text
    return drug_dict

for i in range(5):
    drug = Drug(pk=1)
    print(drug)