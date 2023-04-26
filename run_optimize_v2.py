import argparse
from optimize_algoritm_v2.division_dirs import DivisionDirs

parser = argparse.ArgumentParser(description='Paths for dirs')

parser.add_argument('path_input', help='Path to directory with input images')

parser.add_argument('path_output', help='Path to directory where save markup dataset')

args = parser.parse_args()

DivisionDirs(input_path=args.path_input, output_path=args.path_output)