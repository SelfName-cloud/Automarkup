from module_division.division import DivisionDirs
import argparse

parser = argparse.ArgumentParser(description='Paths for dirs')

parser.add_argument('path_input', help='Path to directory with input images')

parser.add_argument('path_output', help='Path to directory where save markup dataset')

args = parser.parse_args()

division_dirs = DivisionDirs(path_dir_input=args.path_input, path_dir_output=args.path_output)

division_dirs.make_new_dir()