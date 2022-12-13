from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from rls_parser_methods import get_drug_info, rls_authorization
from rls_parser_settings import AUTH_DATA, AUTH_URL
import os
import sys
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DataError
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(sys.path[0], '../../'))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "drugs_info.drugs_info.settings"
)

import django

django.setup()
from drugs_api.models import Drug, ActiveIngredient

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument((
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63"
    "Safari/537.36"))

print('selenium starting...')
with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
) as browser:
    print('selenium started')
    rls_authorization(browser=browser, auth_url=AUTH_URL, auth_data=AUTH_DATA)
    print('auth')
    COUNT = 0
    browser.implicitly_wait(5)
    sleep(5)
    with open('log.txt', 'r', encoding='UTF-8') as read_file:
        log_links = read_file.readlines()
        for link in log_links:
            link = link.split()[-1]
            sleep(4)
            try:
                data = get_drug_info(browser, link)
                if not data:
                    with open('log_out.txt', 'a', encoding='UTF-8') as f:
                        f.writelines(f"{COUNT} ERROR {link}\n")
                    print(f"count: {COUNT} ERROR {link} <<<<<<<<<<<<<<<<<<<<<")
                    COUNT += 1
                    continue
                try:
                    drug = Drug.objects.get(name=data['name'])
                    drug.pharmacological_class = data['pharmacological_class']
                    drug.form_of_release = data['form_of_release']
                    drug.recipe_only = data.get('recipe_only')
                    drug.save()
                except ObjectDoesNotExist:
                    drug = Drug.objects.create(
                        name=data['name'],
                        pharmacological_class=data['pharmacological_class'],
                        form_of_release=data['form_of_release'],
                        recipe_only=data.get('recipe_only'),
                        )
                    drug.save()

                print((
                    f"id: {drug.id},"
                    f"{data['active_ingredient']},"
                    f"{link}, {COUNT}"))
                COUNT += 1

                if len(data['active_ingredient']) > 0:
                    for item in data['active_ingredient']:
                        try:
                            active_ingredient = ActiveIngredient.objects.get(
                                name=item['name']
                            )
                        except ObjectDoesNotExist:
                            active_ingredient = ActiveIngredient.objects.create(
                                name=item['name']
                            )
                            active_ingredient.save()
                        drug.active_ingredient.add(active_ingredient)
                drug.save()
            except TimeoutException:
                with open('log_out.txt', 'a', encoding='UTF-8') as f:
                    f.writelines(f"'timeout ERROR' {link}\n")
                continue
            except DataError:
                with open('log_out.txt', 'a', encoding='UTF-8') as f:
                    f.writelines(f"'DATA ERROR' {link}\n")
                continue
