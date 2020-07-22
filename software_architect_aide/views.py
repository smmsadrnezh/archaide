from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/')
def dashboard(request):
    context = {'': '', }
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
