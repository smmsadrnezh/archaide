import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from software_architect_aide.common import query, pars_query_all_attribute_tactics
from software_architect_aide.common import visualize, triple_count
from software_architect_aide.models import Architecture
from software_architect_aide.settings import MEDIA_ROOT
from software_architect_aide.queries import ALL_QUALITY_ATTRIBUTES, ALL_QUALITY_ATTRIBUTE_TACTIC


@login_required(login_url='/')
def dashboard(request):
    context = {'architectures': Architecture.objects.filter(owner=request.user)}
    return render(request, 'dashboard_home.html', context)


@login_required(login_url='/')
def architecture_create(request):
    if request.method == 'POST':
        architecture = Architecture(name=request.POST.get('name'), owner=request.user)
        if request.FILES.get('ontology'):
            architecture.owl_file = request.FILES.get('ontology')
            architecture.save()
            image_path = os.path.join(MEDIA_ROOT, 'visual', architecture.owl_file.name + '.png')
            rdf_path = architecture.owl_file.path
            architecture.triple_count = triple_count(rdf_path)
            visualize(rdf_path, image_path)
        else:
            pass
        architecture.save()
        context = {'success': True}
        return render(request, 'dashboard_architecture_create.html', context)
    else:
        context = {'': ''}
        return render(request, 'dashboard_architecture_create.html', context)


@login_required(login_url='/')
def architecture_delete(request, architecture_id):
    architecture = Architecture.objects.get(id=architecture_id)
    if request.method == 'POST':
        architecture.delete()
    return HttpResponseRedirect('/dashboard')


@login_required(login_url='/')
def architecture_edit(request):
    return None


@login_required(login_url='/')
def tradeoff(request):
    context = {'': '', }
    return render(request, 'dashboard_tradeoff.html', context)


@login_required(login_url='/')
def evolution(request):
    context = {'': '', }
    return render(request, 'dashboard_evolution.html', context)


@login_required(login_url='/')
def get_reference_architecture(request):
    # quality_attributes = query(ALL_QUALITY_ATTRIBUTES)
    query_result = query(ALL_QUALITY_ATTRIBUTE_TACTIC)
    qa_t = pars_query_all_attribute_tactics(query_result)
    qa_list = ['Security', 'Performance']
    result = dict()
    for qa in qa_list:
        result.update({qa: []})
    for item in qa_t:
        key = list(item.keys())[0]
        value = list(item.values())[0]
        if key in result.keys():
            result[key].append(value)
    return render(request, 'dashboard_architecture_create.html', context={'data': qa_t})
