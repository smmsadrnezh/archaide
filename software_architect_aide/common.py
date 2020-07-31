import subprocess

from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import OWL, RDF, RDFS
from rdflib import Literal

import software_architect_aide.visualize
from software_architect_aide.local_settings import BASE_DIR
from software_architect_aide.queries import CONCERNS

MANUAL_ONTOLOGY_PATH = BASE_DIR + '/data/owl/manual_ontology.owl'
REFERENCE_ONTOLOGY_PATH = BASE_DIR + '/data/owl/ontology.owl'
BASE_URI = "http://archaide.ml/ontology#"


def create_instances(instances_name, class_name, owl_path):
    for instance_name in instances_name:
        instance = URIRef(BASE_URI + instance_name)
        class_ = URIRef(BASE_URI + class_name)
        g = Graph()
        name = Literal(instance_name)
        g.parse(owl_path, format='application/rdf+xml', )
        g.bind("owl", OWL)
        g.add((instance, RDF.type, class_))
        g.add((instance, RDFS.label, name))
        g.serialize(destination=owl_path, format="application/rdf+xml")


def visualize(rdf_path, image_path):
    dot_path = image_path.replace('.png', '.dot')
    software_architect_aide.visualize.main(rdf_path, dot_path)
    bash_command = "dot -Tpng -o {} {}".format(image_path, dot_path)
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    process.communicate()


def axiom_count(rdf_path):
    rdf_graph = Graph().parse(rdf_path)
    return len(rdf_graph)


def query_reference(query_string):
    g = Graph()
    g.parse(BASE_DIR + "/data/owl/ontology.owl", format='xml')
    return g.query(query_string)


def query_manual(query_string, owl_path):
    g = Graph()
    g.parse(owl_path, format='xml')
    return g.query(query_string)


def pars_query_all_attributes(query_result):
    return [row.asdict()['qalabel'].value for row in query_result]


def pars_query_two_label(query_result):
    return [(row.asdict()['qalabel'].value, row.asdict()['tlabel'].value) for row in query_result]


def pars_query_all_attribute_tactics(query_result):
    qa_t = list()
    for row in query_result:
        qa_t.append({row.asdict()['qa_label'].value: row.asdict()['tactic_label'].value})
    return qa_t


def pars_patterns_tactic_label(query_result):
    return [(row.asdict()['tlabel'].value, row.asdict()['plabel'].value) for row in query_result]


def triple_count(rdf_path):
    return len(Graph().parse(rdf_path))


def create_comprises_augments(tuples, owl_path):
    pairs = tuple(tuples)
    for pair in pairs:
        pattern_instance = URIRef(BASE_URI + pair[0])
        tactic_instance = URIRef(BASE_URI + pair[1])
        comprises_rel = URIRef(BASE_URI + "comprises")
        augments_rel = URIRef(BASE_URI + "augments")
        g = Graph()
        g.parse(owl_path, format='application/rdf+xml', )
        g.bind("owl", OWL)
        g.add((pattern_instance, comprises_rel, tactic_instance))
        g.add((tactic_instance, augments_rel, pattern_instance))
        g.serialize(destination=owl_path, format="application/rdf+xml")


def create_is_achieved_by_achieves(tuples, owl_path):
    pairs = tuple(tuples)
    for pair in pairs:
        concern_instance = URIRef(BASE_URI + pair[0])
        tactic_instance = URIRef(URIRef(BASE_URI + pair[1]))
        is_achieved_by_rel = URIRef(BASE_URI + "isAchievedBy")
        achieves_rel = URIRef(BASE_URI + "achieves")
        g = Graph()
        g.parse(owl_path, format='application/rdf+xml', )
        g.bind("owl", OWL)
        g.add((concern_instance, is_achieved_by_rel, tactic_instance))
        g.add((tactic_instance, achieves_rel, concern_instance))
        g.serialize(destination=owl_path, format="application/rdf+xml")


def get_concerns(owl_path):
    g = Graph()
    g.parse(owl_path, format='application/rdf+xml', )
    g.bind("owl", OWL)
    query_result = query_manual(CONCERNS, owl_path)
    return pars_concerns_query(query_result)


def pars_concerns_query(query_result):
    result = list()
    for row in query_result:
        uri = str(row.asdict()["subject"])
        result.append(uri[uri.index("#") + 1:])

    return result


def export(source_path, serializer, export_path):
    g = Graph()
    g.parse(source_path, format='application/rdf+xml', )
    g.bind("owl", OWL)

    g.serialize(destination=export_path, format=serializer)


def pars_relation_label(query_result):
    return [row.asdict()['relation_label'].value for row in query_result]


def pars_concern_decision(query_result):
    return [(row.asdict()['concern_label'].value, row.asdict()['decision_label'].value) for row in query_result]
