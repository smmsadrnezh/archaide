import matplotlib.pyplot as plt
import networkx as nx
from rdflib import Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph

from software_architect_aide.local_settings import BASE_DIR
from software_architect_aide.queries import ALL_QUALITY_ATTRIBUTES


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


def query():
    g = Graph()
    g.parse(BASE_DIR + "/data/owl/ontology.owl", format='xml')
    result = g.query(ALL_QUALITY_ATTRIBUTES)
    for row in result:
        print("%s knows %s" % row)


def triple_count(rdf_path):
    return len(Graph().parse(rdf_path))
