import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from software_architect_aide.common import query, pars_query_all_attribute_tactics, create_instances
from software_architect_aide.common import visualize, triple_count
from software_architect_aide.models import Architecture
from software_architect_aide.queries import ALL_QUALITY_ATTRIBUTE_TACTIC
from software_architect_aide.settings import MEDIA_ROOT
from software_architect_aide.utils import get_random_string
from shutil import copyfile
from .common import MANUAL_ONTOLOGY_PATH


@login_required(login_url='/')
def dashboard(request):
    context = {'architectures': Architecture.objects.filter(owner=request.user)}
    return render(request, 'dashboard_home.html', context)


@login_required(login_url='/')
def create_upload(request):
    if request.method == 'POST':
        request.POST.get('name')
        architecture = Architecture(name=request.POST.get('name'), owner=request.user)
        architecture.owl_file = request.FILES.get('ontology')
        architecture.save()
        image_path = os.path.join(MEDIA_ROOT, 'visual', architecture.owl_file.name + '.png')
        rdf_path = architecture.owl_file.path
        architecture.triple_count = triple_count(rdf_path)
        visualize(rdf_path, image_path)
        architecture.save()
        context = {'success': True}
        return render(request, 'dashboard_create_upload.html', context)
    else:
        return render(request, 'dashboard_create_upload.html')


@login_required(login_url='/')
def create_reference(request):
    query_result = query(ALL_QUALITY_ATTRIBUTE_TACTIC)
    qa_t = pars_query_all_attribute_tactics(query_result)
    context = {'data': qa_t}
    return render(request, 'dashboard_create_reference.html', context)


@login_required(login_url='/')
def create_manual(request):
    context = {}
    if request.method == 'POST':

        current_step = int(request.POST.get('step'))
        if current_step == 1:

            quality_list = request.POST.getlist('quality[]')
            business_list = request.POST.getlist('business[]')
            risk_list = request.POST.getlist('risk[]')

            random_string = 'manual_' + get_random_string()
            owl_path = os.path.join(MEDIA_ROOT, 'owl', random_string + '.owl')
            copyfile(MANUAL_ONTOLOGY_PATH, owl_path)

            architecture = Architecture(owl_file=owl_path, owner=request.user)
            architecture.save()

            create_instances(quality_list, 'Quality_Attribute', owl_path)
            # create_instances(business_list, 'Business_Need', owl_path)
            # create_instances(risk_list, 'Risk_Mitigation', owl_path)

            context = {'current_step': current_step + 1}

        elif current_step == 2:

            pattern_list = request.POST.getlist('pattern[]')
            tactic_list = request.POST.getlist('tactic[]')

            owl_path = Architecture.objects.filter(owner=request.user)[-1].owl_file.path

            create_instances(pattern_list, 'Pattern', owl_path)
            create_instances(tactic_list, 'Tactic', owl_path)

            context = {'current_step': current_step + 1}

        elif current_step == 3:
            architecture = Architecture.objects.filter(owner=request.user).latest('id')
            architecture.name = request.POST.get('name')
            HttpResponseRedirect('/dashboard')

    else:
        context = {'current_step': 1}
    return render(request, 'dashboard_create_manual.html', context)


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

# @login_required(login_url='/')
# def get_reference_architecture(request):
#     # quality_attributes = query(ALL_QUALITY_ATTRIBUTES)
#     query_result = query(ALL_QUALITY_ATTRIBUTE_TACTIC)
#     qa_t = pars_query_all_attribute_tactics(query_result)
#     qa_list = ['Security', 'Performance']
#     result = dict()
#     for qa in qa_list:
#         result.update({qa: []})
#     for item in qa_t:
#         key = list(item.keys())[0]
#         value = list(item.values())[0]
#         if key in result.keys():
#             result[key].append(value)
#     return render(request, 'dashboard_create_upload.html', context={'data': qa_t})
