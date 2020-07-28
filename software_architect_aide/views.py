import os
from shutil import copyfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .common import MANUAL_ONTOLOGY_PATH, create_comprises_augments, create_is_achieved_by_achieves, get_concerns, \
    export, pars_query_all_attributes, query_reference
from .common import pars_query_all_attribute_tactics, create_instances
from .common import visualize, triple_count
from .models import Architecture
from .queries import ALL_QUALITY_ATTRIBUTE_TACTIC, ALL_QUALITY_ATTRIBUTES
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

            instances = {'patterns': pattern_list, 'tactics': tactic_list, 'concerns': get_concerns(owl_path)}
            context = {'instances': instances, 'current_step': current_step + 1}

        elif current_step == 3:

            comprises_pattern = request.POST.getlist('comprises_pattern[]')
            comprises_tactic = request.POST.getlist('comprises_tactic[]')

            is_achieved_by_concern = request.POST.getlist('is_achieved_by_concern[]')
            is_achieved_by_tactic = request.POST.getlist('is_achieved_by_tactic[]')

            comprises = zip(comprises_pattern, comprises_tactic)
            is_achieved_by = zip(is_achieved_by_concern, is_achieved_by_tactic)

            owl_path = Architecture.objects.filter(owner=request.user).latest('id').owl_file.path
            create_comprises_augments(comprises, owl_path)
            create_is_achieved_by_achieves(is_achieved_by, owl_path)

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
    context = {}
    if request.method == 'POST':
        current_step = int(request.POST.get('step'))
        if current_step == 1:
            pass

        elif current_step == 2:
            # quality_attributes = request.POST.get('quality_attributes')
            quality_attributes = ['Performance', 'Security']
            selected_qa = ""
            for quality_attribute in quality_attributes:
                quality_attribute = f":{quality_attribute}"
            selected_qa = ' , '.join(quality_attributes)
            query_part1 = """
            SELECT ?subject ?object
                WHERE
                { 
                 ?subject a :Tactic.
                ?object a :Quality_Attribute.
                 ?subject rdfs:label ?tlabel.
                ?object rdfs:label ?qalabel.
                ?subject :achieves ?object
                Filter (?object in (:Security , :Performance) )
                }
            ORDER BY ?object ?subject
            """
            query_part2 = f"{selected_qa}" + """)
                }
            ORDER BY ?object ?subject"""
            query = query_part1 + query_part2
            query_result = query_reference(query)
            qa = pars_query_all_attributes(query_result)
            context = {'qa': qa}

        elif current_step == 3:
            pass

        elif current_step == 4:
            pass
    else:
        query_result = query_reference(ALL_QUALITY_ATTRIBUTES)
        qa = pars_query_all_attributes(query_result)
        context = {'qa': qa}
    return render(request, 'dashboard_create_reference.html', context)


@login_required(login_url='/')
def architecture_delete(request, architecture_id):
    architecture = Architecture.objects.get(id=architecture_id)
    if request.method == 'POST':
        architecture.delete()
    return HttpResponseRedirect('/dashboard')


@login_required(login_url='/')
def architecture_export(request, architecture_id):
    if request.method == 'GET':
        architecture = Architecture.objects.get(id=architecture_id)
        if request.user == architecture.owner:
            source_path = architecture.owl_file.path
            serializer = request.GET.get('serializer')
            export_path = '{}.{}.owl'.format(source_path, serializer)
            export(source_path, serializer, export_path)
            export_url = '{}.{}.owl'.format(architecture.owl_file.url, serializer)
            return HttpResponseRedirect(export_url)
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


@login_required(login_url='/')
def report(request, file_name):
    if file_name == "html":
        return render(request, "ontospy/html/index.html")
    if file_name == "html_multi":
        return render(request, "ontospy/html_multi/index.html")
    if file_name == "rotating_cluster":
        return render(request, "ontospy/rotating_cluster/index.html")
    if file_name == "tree":
        return render(request, "ontospy/tree/index.html")
    if file_name == "partition_table":
        return render(request, "ontospy/partition_table/index.html")
