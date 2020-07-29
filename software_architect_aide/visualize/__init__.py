import argparse
import json
from software_architect_aide.local_settings import BASE_DIR
from software_architect_aide.visualize.ontology_viz import OntologyGraph
from software_architect_aide.visualize.utils import Config

CONFIG_PATH = BASE_DIR + '/software_architect_aide/visualize/config.json'


def main(rdf_path, dot_path):
    args = argparse.Namespace(config=CONFIG_PATH, files=[rdf_path], format='xml', out=dot_path, ontology=None)
    config = Config(args.config)
    og = OntologyGraph(args.files, config, args.format, ontology=args.ontology)
    og.write_file(args.out)
