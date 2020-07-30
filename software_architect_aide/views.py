import os
from shutil import copyfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .common import MANUAL_ONTOLOGY_PATH, create_comprises_augments, create_is_achieved_by_achieves, get_concerns, \
    query_reference, pars_patterns_tactic_label, query_manual, pars_concerns_query, pars_relation_label
from .common import create_instances
from .common import export, pars_query_all_attributes, pars_query_two_label
from .common import visualize, triple_count
from .models import Architecture
from .queries import ALL_QUALITY_ATTRIBUTES, SELECTED_QUALITY_ATTRIBUTES
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

            context = {'current_step': current_step + 1, 'architecture': architecture}

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

            file_name = 'reference_{}.owl'.format(get_random_string())
            owl_path = os.path.join(settings.MEDIA_ROOT, 'owl', file_name)
            copyfile(MANUAL_ONTOLOGY_PATH, owl_path)

            architecture = Architecture(owner=request.user, creation_method='reference')
            architecture.owl_file.name = os.path.join('owl', file_name)
            architecture.save()

            qualities = request.POST.getlist('quality[]')

            create_instances(qualities, "Quality_Attribute", owl_path)

            selected_qa = ' , '.join([":{}".format(quality) for quality in qualities])
            query_part1 = """
            SELECT ?tlabel ?qalabel
                WHERE
                    {{
                        ?subject a :Tactic .
                        ?object a :Quality_Attribute .
                        ?subject rdfs:label ?tlabel .
                        ?object rdfs:label ?qalabel .
                        ?subject :achieves ?object .
                        Filter (?object in ({}))
                    }} ORDER BY ?tlabel ?qalabel""".format(selected_qa)
            query_result = query_reference(query_part1)
            quality_tactics = pars_query_two_label(query_result)

            quality_tactics_dict = {quality_tactic[0]: [] for quality_tactic in quality_tactics}
            for quality_tactic in quality_tactics:
                quality_tactics_dict[quality_tactic[0]].append(quality_tactic[1])
            context = {'current_step': current_step + 1, 'quality_tactics_dict': quality_tactics_dict}

        elif current_step == 2:
            quality_tactics = request.POST.getlist('tactic[]')
            owl_path = Architecture.objects.filter(owner=request.user).latest('id').owl_file.path
            parsed_quality_tactics = list()
            for quality_tactic in quality_tactics:
                temp = quality_tactic.split(',')
                temp[1] = temp[1].replace(' ', '_')
                parsed_quality_tactics.append((temp[0], temp[1]))
            tactics = [parsed_quality_tactic[1] for parsed_quality_tactic in parsed_quality_tactics]
            create_instances(tactics, "Tactic", owl_path)
            create_is_achieved_by_achieves(parsed_quality_tactics, owl_path)

            # Show related patterns
            selected_tactic = ' , '.join([":{}".format(quality_tactic[1]) for quality_tactic in parsed_quality_tactics])

            query = """
            SELECT ?tlabel ?plabel
                WHERE
                    {{
                        ?subject a :Pattern .
                        ?object a :Tactic .
                        ?subject rdfs:label ?plabel .
                        ?object rdfs:label ?tlabel .
                        ?subject :comprises ?object .
                        Filter (?object in ({}))
                    }} ORDER BY ?tlabel ?plabel""".format(selected_tactic)
            query_result = query_reference(query)
            pattern_tactics = pars_patterns_tactic_label(query_result)

            pattern_tactics_dict = {pattern_tactic[0]: [] for pattern_tactic in pattern_tactics}
            for pattern_tactic in pattern_tactics:
                pattern_tactics_dict[pattern_tactic[0]].append(pattern_tactic[1])
            context = {'current_step': current_step + 1, 'pattern_tactics_dict': pattern_tactics_dict}

        elif current_step == 3:
            owl_path = Architecture.objects.filter(owner=request.user).latest('id').owl_file.path
            tactic_patterns = list()
            tactic_counter = request.POST.get('tactic_counter')
            for counter in range(1, int(tactic_counter if tactic_counter else 0) + 1):
                tactic_patterns += request.POST.getlist('pattern[{}]'.format(counter))
            tactic_patterns = [tactic_pattern.replace(' ', '_') for tactic_pattern in tactic_patterns]
            patterns = [tactic_pattern.split(',')[1] for tactic_pattern in tactic_patterns]
            create_instances(patterns, "Pattern", owl_path)
            tuples = list()
            for tactic_pattern in tactic_patterns:
                temp = tactic_pattern.split(',')
                tuples.append((temp[0], temp[1]))

            create_comprises_augments(tuples, owl_path)
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
        query_result = query_reference(ALL_QUALITY_ATTRIBUTES)
        qualities = pars_query_all_attributes(query_result)
        context = {'current_step': 1, 'qualities': qualities}
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
def tradeoff(request):
    architecture_id = request.GET.get("architecture_id")
    if architecture_id:
        architecture = get_object_or_404(Architecture, owner=request.user, id=architecture_id)
        owl_path = architecture.owl_file

        query_result = query_manual(SELECTED_QUALITY_ATTRIBUTES, owl_path)
        qualities = pars_concerns_query(query_result)
        context = {'architecture': architecture, 'quality_relations': {}}

        relation_color = {'hasNoEffectOn': 'yellow', 'isWeakenedBy': 'red', 'strengthen': 'green', 'weaken': 'red',
                          'isStrengthenedBy': 'green'}
        for quality in qualities:
            for quality2 in qualities:
                if quality != quality2:
                    query = """
                    SELECT ?relation_label WHERE
                    {{ 
                        :{} ?rel :{}.
                        ?rel rdfs:label ?relation_label.
                    }}
                    ORDER BY ?relation
                    """.format(quality, quality2)
                    query_result = query_reference(query)
                    relations = [(relation, relation_color[relation]) for relation in pars_relation_label(query_result)]
                    context['quality_relations'][(quality, quality2)] = relations

        return render(request, "dashboard_tradeoff.html", context)
    else:
        return HttpResponseRedirect('/dashboard')


@login_required(login_url='/')
def evolution(request):
    context = {'': '', }
    return render(request, 'dashboard_evolution.html', context)


@login_required(login_url='/')
def ontospy_report(request):
    context = {}
    return render(request, 'dashboard_ontospy_report.html', context)


@login_required(login_url='/')
def report(request, report_name):
    if report_name == "html":
        return render(request, "ontospy/html/index.html")
    elif report_name == "rotating_cluster":
        return render(request, "ontospy/rotating_cluster/index.html")
    elif report_name == "tree":
        return render(request, "ontospy/tree/index.html")
    elif report_name == "partition_table":
        return render(request, "ontospy/partition_table/index.html")


@login_required(login_url='/')
def delete_all_architectures(request):
    Architecture.objects.filter(owner=request.user).delete()
    return render(request, "dashboard_home.html")


@login_required(login_url='/')
def report_multi_index(request):
    return render(request, "ontospy/html_multi/index.html")


@login_required(login_url='/')
def report_multi(request, file_name):
    template = "ontospy/html_multi/{}".format(file_name)
    return render(request, template)
