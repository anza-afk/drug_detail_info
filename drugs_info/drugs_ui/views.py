from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import redirect, render
import requests
from .forms import DrugForm
import json

# URL need to change
URL = 'http://127.0.0.1:8000/api/v1/drugs/'


def index(request, name):
    response = requests.get(f'{URL}drug/detail/{name}', headers={})
    drug_json = response.json()
    return render(request, 'drugs_ui/index.html', {"drug_json": drug_json})


def add_drug(request):
    endpoint = f'{URL}drug/create'
    if request.method == 'POST':
        form = DrugForm(request.POST)  # request.user
        if form.is_valid():
            active_ingredient = [
                {"name": x.strip()} for x in form['active_ingredient'].data.split(',')
            ]
            array = {
                'name': form['name'].data,
                'active_ingredient': active_ingredient,
                'minimal_age': form['minimal_age'].data,
                'recipe_only': form['recipe_only'].data,
                'form_of_release': form['form_of_release'].data
            }
            array = json.dumps(array)
            requests.post(
                endpoint,
                data=array,
                headers={'Content-Type': 'application/json'}
            )
            form = DrugForm()
            return render(request, 'drugs_ui/put_form.html', {'form': form})
    else:
        form = DrugForm()  # request.user
    return render(request, 'drugs_ui/put_form.html', {'form': form})


def drug_search_by_component(request, search_type, component):
    if search_type in ('ingredient', 'drug'):
        response = requests.get(f'{URL}{search_type}/{component}', headers={})
        drug_json = response.json()
        return render(
            request,
            'drugs_ui/component_list.html',
            {"drug_json": drug_json}
            )
    else:
        return HttpResponseNotFound(f'Неверные параметры поиска: {search_type}')
