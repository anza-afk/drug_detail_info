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
from django.db.utils import IntegrityError

sys.path.append(os.getcwd())
sys.path.append(os.path.join(sys.path[0], '../../'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drugs_info.drugs_info.settings")

import django
django.setup()

from drugs_api.models import DrugLink, Drug, ActiveIngredient

options = Options()
options.add_argument("--headless")


with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
    ) as browser:
    rls_authorization(browser=browser, auth_url=AUTH_URL, auth_data=AUTH_DATA)
    browser.implicitly_wait(2)
    for link in DrugLink.objects.all()[:5]:
        data = get_drug_info(browser, link.url)
        try:
            drug = Drug(
                name=data['name'],
                pharmacological_class=data['pharmacological_class'],
                form_of_release=data['form_of_release'],
                recipe_only=data['recipe_only'],
                )
            
            drug.save()
            link.drug_id=drug
            link.save()
            if len(data['active_ingredient']) > 0:
                for item in data['active_ingredient']:
                    active_ingredient = ActiveIngredient(name=item['name'])
                    active_ingredient.save()
                    drug.active_ingredient.add(active_ingredient)
            drug.save()
            
        except IntegrityError:
            continue
