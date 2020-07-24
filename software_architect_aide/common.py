import matplotlib.pyplot as plt
import networkx as nx
from rdflib import Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph

from software_architect_aide.local_settings import BASE_DIR


def create_instances(instances, class_name, owl_path):
    # TODO
    pass


def visualize(rdf_path, image_path):
    rdf_graph = Graph().parse(rdf_path)
    G = rdflib_to_networkx_multidigraph(rdf_graph)

    # Plot Networkx instance of RDF Graph
    pos = nx.spring_layout(G, scale=2)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos, labels=edge_labels)
    nx.draw(G, with_labels=True)
    plt.savefig(image_path)


def axiom_count(rdf_path):
    rdf_graph = Graph().parse(rdf_path)
    return len(rdf_graph)


def query(query_string):
    g = Graph()
    g.parse(BASE_DIR + "/data/owl/ontology.owl", format='xml')
    return g.query(query_string)


def pars_query_all_attributes(query_result):
    quality_attributes = list()
    for row in query_result:
        quality_attributes.append(row.asdict()['qalabel'].value)
    return quality_attributes


def pars_query_all_attribute_tactics(query_result):
    qa_t = list()
    for row in query_result:
        qa_t.append({row.asdict()['qa_label'].value: row.asdict()['tactic_label'].value})
    return qa_t


def triple_count(rdf_path):
    return len(Graph().parse(rdf_path))


def get_all_tactic_by_qa(quality_attributes, qa_t):
    for item in qa_t:
        pass
