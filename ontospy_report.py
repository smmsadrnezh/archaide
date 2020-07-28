import ontospy
from ontospy.ontodocs.viz.viz_d3partitionTable import Dataviz as Dataviz3
from ontospy.ontodocs.viz.viz_d3rotatingCluster import Dataviz as Dataviz2
from ontospy.ontodocs.viz.viz_d3tree import Dataviz
from ontospy.ontodocs.viz.viz_html_multi import KompleteViz
from ontospy.ontodocs.viz.viz_html_single import HTMLVisualizer
import shutil
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
    v.build(output_path=BASE_DIR + '/templates/ontospy/html')
    shutil.move("templates/ontospy/html/static", "software_architect_aide/static/html_static")
    # v.preview()

    v = KompleteViz(manual_graph)
    v.build(output_path=BASE_DIR + '/templates/ontospy/html_multi')
    shutil.move("templates/ontospy/html_multi/static", "software_architect_aide/static/html_multi_static")
    # v.preview()

    v = Dataviz(manual_graph)
    v.build(output_path=BASE_DIR + '/templates/ontospy/tree')
    shutil.move("templates/ontospy/tree/static", "software_architect_aide/static/tree_static")
    # v.preview()

    v = Dataviz2(manual_graph)
    v.build(output_path=BASE_DIR + '/templates/ontospy/rotating_cluster')
    shutil.move("templates/ontospy/rotating_cluster/static", "software_architect_aide/static/rotating_cluster_static")
    # v.preview()

    v = Dataviz3(manual_graph)
    v.build(output_path=BASE_DIR + '/templates/ontospy/partition_table')
    shutil.move("templates/ontospy/partition_table/static", "software_architect_aide/static/partition_table_static")
    # v.preview()
