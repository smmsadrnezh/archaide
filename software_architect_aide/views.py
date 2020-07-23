from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rdflib import Graph

from software_architect_aide.models import Architecture


@login_required(login_url='/')
def dashboard(request):
    context = {'architectures': Architecture.objects.filter(owner=request.user)}
    return render(request, 'dashboard_home.html', context)


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
        architecture = Architecture(name=request.POST.get('name'), owner=request.user)
        if request.FILES.get('ontology'):
            architecture.owl_file = request.FILES.get('ontology')
            architecture.save()
            architecture.axiom_count = len(Graph().parse(architecture.owl_file.path))
        else:
            pass
        architecture.save()
        return redirect('dashboard')
    else:
        context = {'': '', }
        return render(request, 'dashboard_architecture_create.html', context)


@login_required(login_url='/')
def architecture_delete(request):
    return None
