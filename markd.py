from rich.markdown import Markdown
from rich.console import Console

import click

console = Console()

@click.command()
@click.option("-l", '--length', default=16, help='How long do you want it ? (Length of the password) ')
@click.option("-t", '--type', default="normal", help='How twisted do you want it ? \n\tVanilla (Only with letters) ? \n\tHard (Letters + Numbers) ? Super twisted (All at once with extra specials on top !)')
@click.option("-n", '--number', default=16, help='How many do you want at the same time ? (Default on 1)')
@click.option("-ns", "--no-sep", help="Remove the separator (default on '-') from the password")
@click.option("-low", "--lower", help="Transform the output in lowercase")
@click.option("-o", "--output", help="The path to an output file to send the result to. (Most text formats accepted but better choose '.txt')")
def markd(length: int = 16, 
          type : str = "normal", 
          number: int = 1, 
          no_separator : bool = False, 
          lower : bool = False, 
          output: str = None):


md = Markdown("""
# Welcome
This is **Rich** rendering _Markdown_ content beautifully.
""")

console.print(md)