from rich.console import Console
from rich.markdown import Markdown
import argparse


parser = argparse.ArgumentParser(description='Fancy MD')
parser.add_argument('-o', '--output', type=str, help='The file to read')
args = parser.parse_args()

if args.output:
    output = args.output
else:
    output = input('Enter the output file: ')

with open(output, 'r') as f:

    data = f.read()

    console = Console()
    md = Markdown(data)
    console.print(md)