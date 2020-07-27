import os
from shutil import copyfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .common import MANUAL_ONTOLOGY_PATH, create_comprises, create_is_achieved_by
from .common import query, pars_query_all_attribute_tactics, create_instances
from .common import visualize, triple_count
from .models import Architecture
from .queries import ALL_QUALITY_ATTRIBUTE_TACTIC
from .utils import get_random_string


@login_required(login_url='/')
def dashboard(request):
    context = {'architectures': Architecture.objects.filter(owner=request.user)}
    return render(request, 'dashboard_home.html', context)


@login_required(login_url='/')
def create_upload(request):
    if request.method == 'POST':
        architecture = Architecture(name=request.POST.get('name'), owner=request.user, creation_method='upload',
                                    owl_file=request.FILES.get('ontology'))
        architecture.save()
        image_path = os.path.join(settings.MEDIA_ROOT, 'visual', architecture.owl_file.name + '.png')
        rdf_path = architecture.owl_file.path
        architecture.triple_count = triple_count(rdf_path)
        visualize(rdf_path, image_path)
        architecture.save()
        context = {'success': True}
        return render(request, 'dashboard_create_upload.html', context)
    else:
        return render(request, 'dashboard_create_upload.html', {})


@login_required(login_url='/')
def create_manual(request):
    context = {}
    if request.method == 'POST':
        current_step = int(request.POST.get('step'))
        if current_step == 1:

            quality_list = request.POST.getlist('quality[]')
            business_list = request.POST.getlist('business[]')
            risk_list = request.POST.getlist('risk[]')

            file_name = 'manual_{}.owl'.format(get_random_string())
            owl_path = os.path.join(settings.MEDIA_ROOT, 'owl', file_name)
            copyfile(MANUAL_ONTOLOGY_PATH, owl_path)

            architecture = Architecture(owner=request.user, creation_method='manual')
            architecture.owl_file.name = os.path.join('owl', file_name)
            architecture.save()

            create_instances(quality_list, 'Quality_Attribute', owl_path)
            create_instances(business_list, 'Business_Need', owl_path)
            create_instances(risk_list, 'Risk_Mitigation', owl_path)

            context = {'current_step': current_step + 1, 'fields': [['pattern', 'الگو'], ['tactic', 'راهکنش']]}

        elif current_step == 2:

            pattern_list = request.POST.getlist('pattern[]')
            tactic_list = request.POST.getlist('tactic[]')

            owl_path = Architecture.objects.filter(owner=request.user).latest('id').owl_file.path

            create_instances(pattern_list, 'Pattern', owl_path)
            create_instances(tactic_list, 'Tactic', owl_path)

            concerns = 0

            instances = {'patterns': pattern_list, 'tactics': tactic_list, 'concerns': concerns}
            context = {'instances': instances, 'current_step': current_step + 1}

        elif current_step == 3:

            comprises_pattern = request.POST.getlist('comprises_pattern[]')
            comprises_tactic = request.POST.getlist('comprises_tactic[]')

            is_achieved_by_concern = request.POST.getlist('is_achieved_by_concern[]')
            is_achieved_by_tactic = request.POST.getlist('is_achieved_by_tactic[]')

            comprises = zip(comprises_pattern, comprises_tactic)
            is_achieved_by = zip(is_achieved_by_concern, is_achieved_by_tactic)

            owl_path = Architecture.objects.filter(owner=request.user).latest('id').owl_file.path
            # TODO: Create Instances
            create_comprises(comprises, owl_path)
            create_is_achieved_by(is_achieved_by, owl_path)

            architecture = Architecture.objects.filter(owner=request.user).latest('id')
            rdf_path = architecture.owl_file.path
            architecture.triple_count = triple_count(rdf_path)
            architecture.save()

            image_path = os.path.join(settings.MEDIA_ROOT, 'visual', architecture.owl_file.name + '.png')
            visualize(rdf_path, image_path)

            context = {'current_step': current_step + 1}

        elif current_step == 4:
            architecture = Architecture.objects.filter(owner=request.user).latest('id')
            architecture.name = request.POST.get('name')
            architecture.save()
            context = {'success': True, 'current_step': 1}

    else:
        context = {'current_step': 1,
                   'fields': [['risk', 'مخاطره'], ['quality', 'ویژگی کیفی'], ['business', 'نیازمندی حرفه']]}
    return render(request, 'dashboard_create_manual.html', context)


@login_required(login_url='/')
def create_reference(request):
    if request.method == 'POST':
        context = {}
    else:
        query_result = query(ALL_QUALITY_ATTRIBUTE_TACTIC)
        qa_t = pars_query_all_attribute_tactics(query_result)
        context = {'data': qa_t}
    return render(request, 'dashboard_create_reference.html', context)


@login_required(login_url='/')
def architecture_delete(request, architecture_id):
    architecture = Architecture.objects.get(id=architecture_id)
    if request.method == 'POST':
        architecture.delete()
    return HttpResponseRedirect('/dashboard')


@login_required(login_url='/')
def architecture_export(request, architecture_id):
    if request.method == 'POST':
        architecture = Architecture.objects.get(id=architecture_id)
        if request.user == architecture.owner:
            pass
    return HttpResponseRedirect('/dashboard')


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

@login_required(login_url='/')
def ontospy_report(request):
    context = {}
    return render(request, 'dashboard_ontospy_report.html', context)
