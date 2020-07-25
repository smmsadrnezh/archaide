import ontospy
from ontospy.ontodocs.viz.viz_d3partitionTable import Dataviz as Dataviz3
from ontospy.ontodocs.viz.viz_d3rotatingCluster import Dataviz as Dataviz2
from ontospy.ontodocs.viz.viz_d3tree import Dataviz
from ontospy.ontodocs.viz.viz_html_multi import KompleteViz
from ontospy.ontodocs.viz.viz_html_single import HTMLVisualizer

from software_architect_aide.local_settings import BASE_DIR

if __name__ == "__main__":
    reference_path = BASE_DIR + '/data/owl/ontology.owl'
    manual_path = BASE_DIR + '/data/owl/manual_ontology.owl'

    manual_graph = ontospy.Ontospy(manual_path)
    reference_graph = ontospy.Ontospy(reference_path)

    m_stats = manual_graph.stats()
    r_stats = reference_graph.stats()
    with open(BASE_DIR + "/data/ontospy/stats/manual_stats.txt", "w") as file:
        file.write(str(m_stats))

    with open(BASE_DIR + "/data/ontospy/stats/reference_stats.txt", "w") as file:
        file.write(str(r_stats))

    v = HTMLVisualizer(manual_graph)
    v.build(output_path=BASE_DIR + '/data/ontospy/html')
    v.preview()

    v = KompleteViz(manual_graph)
    v.build(output_path=BASE_DIR + '/data/ontospy/html_multi')
    v.preview()

    v = Dataviz(manual_graph)
    v.build(output_path=BASE_DIR + '/data/ontospy/tree')
    v.preview()

    v = Dataviz2(manual_graph)
    v.build(output_path=BASE_DIR + '/data/ontospy/rotating_cluster')
    v.preview()

    v = Dataviz3(manual_graph)
    v.build(output_path=BASE_DIR + '/data/ontospy/partition_table')
    v.preview()
