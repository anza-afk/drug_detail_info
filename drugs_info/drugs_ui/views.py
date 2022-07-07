from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import requests
from .forms import DrugForm
import json

# URL need to change
URL = 'http://127.0.0.1:8000/api/v1/drugs/'


class DrugSearch():
    def __init__(self, name: str, active_ingredient: list) -> None:
        self.name = name
        self.active_ingridient = active_ingredient

    def __repr__(self) -> str:
        return self.name


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
            requests.post(endpoint, data=array, headers={'Content-Type': 'application/json'})
            form = DrugForm()
            return render(request, 'drugs_ui/put_form.html', {'form': form})
    else:
        form = DrugForm()  # request.user
    return render(request, 'drugs_ui/put_form.html', {'form': form})


def drug_search(request, component):
    response = requests.get(f'{URL}{component}', headers={})
    drug_json = response.json()
    render_data = []
    # for line in drug_json:
    #     # render_data.append({
    #     #     (line['name']): [x['name'] for x in line['active_ingredient']]
    #     # })
        # render_data.append([
        #     (line['name']), [x['name'] for x in line['active_ingredient']]
        # ])

        # render_data.append(DrugSearch(name = line['name'], active_ingredient = "123"))
        # print(render_data[0].active_ingredient)
    return render(
        request,
        'drugs_ui/component_list.html',
        {"drug_json": drug_json}
        )

