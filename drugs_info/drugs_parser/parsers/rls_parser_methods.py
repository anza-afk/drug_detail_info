from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(sys.path[0], '../../'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drugs_info.settings")

import django
django.setup()
from drugs_api.models import DrugLink


def get_drug_links(browser, url):
    browser.get(url)
    abc_window = browser.find_element(
        By.CLASS_NAME, 'b-alphabet-body').find_element(By.CLASS_NAME, 'head')
    letters = [a.get_attribute('href') for a in abc_window.find_elements(By.TAG_NAME, 'a')]
    for a in letters:
        browser.get(a)
        abc_list = browser.find_element(By.CLASS_NAME, 'b-alphabet-index')
        links = abc_list.find_elements(By.CLASS_NAME, 'link')
        for link in links:
            drug_link = DrugLink(url=link.get_attribute("href"))
            drug_link.save()


def rls_authorization(browser, auth_url, auth_data):
    browser.get(auth_url)
    browser.find_element(By.ID, 'email').send_keys(auth_data['login'])
    browser.find_element(By.ID, 'password').send_keys(auth_data['password'])
    browser.find_element(By.CLASS_NAME, 'btn').click()

    try:
        browser.find_element(By.CLASS_NAME, 'card-header')
        buttons = browser.find_elements(By.CLASS_NAME, 'btn')
        for button in buttons:
            if button.text == 'Продолжить':
                button.click()
    except NoSuchElementException:
        pass

    try:
        title = browser.find_element(By.CLASS_NAME, 'card-header')
        if title.text == 'Выбор аккаунта':
            buttons = browser.find_elements(By.CLASS_NAME, 'btn')
            for button in buttons:
                if button.text == 'Разрешить':
                    button.click()
    except NoSuchElementException:
        pass


def get_drug_info(browser, drug_url):
    browser.get(drug_url)
    try:
        slist = browser.find_element(By.CLASS_NAME, 'structure-list')
        drug_dict = {
            'name': None,
            'active_ingredient': [],
            'pharmacological_class': None,
            'form_of_release': None,
            'recipe_only': None,
        }
        drug_dict['name'] = browser.find_element(By.CLASS_NAME, 'heading').text
        if 'Действующее вещество' in slist.text:
            temp_ingredients = browser.find_element(
                By.XPATH, "//h2[@id='deistvuyushhee-veshhestvo']/following-sibling::div").text
            if '+' in temp_ingredients:
                temp_ingredients = temp_ingredients.replace('IgG+', 'IgG, ').replace('IgA+', 'IgA, ').replace('IgM', 'IgM, ')
                temp_ingredients = re.split('\+|\(', temp_ingredients)
                if len(temp_ingredients) > 1:
                    half_list = int(len(temp_ingredients)/2)
                    for i, v in enumerate(temp_ingredients[:half_list]):
                        ru_name = re.sub('\*|\)', '', v.strip())
                        en_name = re.sub('\*|\)', '', temp_ingredients[half_list + i].strip())
                        drug_dict['active_ingredient'].append(
                            {"name":f"{ru_name} ({en_name})"}
                        )
            else:
                    drug_dict['active_ingredient'].append(
                        {"name":temp_ingredients.strip().replace('*', '')})
        if 'Фармакологическая группа' in slist.text:
            try:
                drug_dict['pharmacological_class'] = browser.find_element(
                    By.XPATH, "//h2[@id='farmakologiceskaya-gruppa']/following-sibling::div").text
            except NoSuchElementException:
                pass
        if 'Форма выпуска' in slist.text:
            try:
                drug_dict['form_of_release'] = browser.find_element(
                    By.XPATH, "//h2[@id='forma-vypuska']/following-sibling::div").text
            except NoSuchElementException:
                pass
        if 'Условия отпуска из аптек' in slist.text:
            try:
                recipe_data = browser.find_element(
                    By.XPATH, "//h2[@id='usloviya-otpuska-iz-aptek']/following-sibling::div").text
                drug_dict['recipe_only'] = True if 'Без' in recipe_data else False
            except NoSuchElementException:
                pass
    except NoSuchElementException:
        drug_dict = False
    return drug_dict
