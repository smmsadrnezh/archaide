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

    v = KompleteViz(manual_graph)
    v.build(output_path=BASE_DIR + '/templates/ontospy/html_multi')
    lines = list()
    with open(BASE_DIR + "/templates/ontospy/html_multi/index.html", 'r') as file:
        lines = file.readlines()

    with open(BASE_DIR + "/templates/ontospy/html_multi/index.html", 'w') as file:
        edited_lines = list()
        for line in lines:
            new_line = line.replace("static/", "/software_architect_aide/static/html_multi/")
            edited_lines.append(new_line)
        file.writelines(edited_lines)

    v = Dataviz(manual_graph)
    v.build(output_path=BASE_DIR + '/templates/ontospy/tree')

    lines = list()
    with open(BASE_DIR + "/templates/ontospy/tree/index.html", 'r') as file:
        lines = file.readlines()

    with open(BASE_DIR + "/templates/ontospy/tree/index.html", 'w') as file:
        edited_lines = list()
        for line in lines:
            new_line = line.replace("static/", "/static/tree/")
            edited_lines.append(new_line)
        file.writelines(edited_lines)

    v = Dataviz2(manual_graph)
    v.build(output_path=BASE_DIR + '/templates/ontospy/rotating_cluster')
    lines = list()
    with open(BASE_DIR + "/templates/ontospy/rotating_cluster/index.html", 'r') as file:
        lines = file.readlines()

    with open(BASE_DIR + "/templates/ontospy/rotating_cluster/index.html", 'w') as file:
        edited_lines = list()
        for line in lines:
            new_line = line.replace("static/", "/static/rotating_cluster/")
            edited_lines.append(new_line)
        file.writelines(edited_lines)

    v = Dataviz3(manual_graph)
    v.build(output_path=BASE_DIR + '/templates/ontospy/partition_table')
    lines = list()
    with open(BASE_DIR + "/templates/ontospy/partition_table/index.html", 'r') as file:
        lines = file.readlines()

    with open(BASE_DIR + "/templates/ontospy/partition_table/index.html", 'w') as file:
        edited_lines = list()
        for line in lines:
            new_line = line.replace("static/", "/static/partition_table/")
            edited_lines.append(new_line)
        file.writelines(edited_lines)

    # move static files
    try:
        shutil.move("templates/ontospy/html/static/", "software_architect_aide/static/")
        shutil.move("templates/ontospy/html_multi/static/", "software_architect_aide/static/html_multi/")
        shutil.move("templates/ontospy/partition_table/static", "software_architect_aide/static/partition_table")
        shutil.move("templates/ontospy/tree/static", "software_architect_aide/static/tree")
        shutil.move("templates/ontospy/rotating_cluster/static",
                    "software_architect_aide/static/rotating_cluster")
    except:
        pass
