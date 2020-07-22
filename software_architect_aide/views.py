from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rdflib import Graph

from software_architect_aide.local_settings import BASE_DIR
from software_architect_aide.models import Architecture


@login_required(login_url='/')
def dashboard(request):
    g = Graph()
    g.parse(BASE_DIR + '/data/owl/ontology.owl')
    context = {'axioms_counts': len(g), 'content': g, 'architectures': Architecture.objects.filter(owner=request.user)}
    return render(request, 'dashboard_home.html', context)


@login_required(login_url='/')
def instantiate(request):
    context = {'': '', }
    return render(request, 'dashboard_instantiate.html', context)


@login_required(login_url='/')
def tradeoff(request):
    context = {'': '', }
    return render(request, 'dashboard_tradeoff.html', context)


@login_required(login_url='/')
def evolution(request):
    context = {'': '', }
    return render(request, 'dashboard_evolution.html', context)


@login_required(login_url='/')
def architecture_edit(request):
    return None


@login_required(login_url='/')
def architecture_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        Architecture.objects.create(name=name, owner=request.user)
        return render(request, 'dashboard_home.html', {'success': 'True'})


@login_required(login_url='/')
def architecture_delete(request):
    return None
