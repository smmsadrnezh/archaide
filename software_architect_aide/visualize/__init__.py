import argparse

from software_architect_aide.visualize.ontology_viz import OntologyGraph
from software_architect_aide.visualize.utils import Config


def main(rdf_path, dot_path):
    args = argparse.Namespace(config=None, files=[rdf_path], format='xml', out=dot_path, ontology=None)
    config = Config(args.config)
    og = OntologyGraph(args.files, config, args.format, ontology=args.ontology)
    og.write_file(args.out)
