from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests
from .forms import DrugForm

# URL need to change
URL = 'http://127.0.0.1:8000/api/v1/drugs/drug/'


def index(request, pk):
    response = requests.get(f'{URL}detail/{pk}', headers={})
    drug_json = response.json()
    return render(request, 'drugs_ui/index.html', {"drug_json": drug_json})


def add_drug(request):
    put_response = f'{URL}create'
    if request.method == 'POST':
        form = DrugForm(request.POST)  # request.user
        if form.is_valid():
            return HttpResponseRedirect('add')
    else:
        form = DrugForm()  # request.user
    return render(request, 'drugs_ui/put_form.html', {'form': form, 'put_response': put_response})