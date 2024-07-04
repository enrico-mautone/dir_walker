import os
import click
from rich.console import Console
from rich.tree import Tree

console = Console()

def display_directory_tree(path):
    tree = Tree(path, guide_style="bold bright_blue")

    def add_directory(tree, path):
        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                branch = tree.add(f"[bold magenta]{item}/[/bold magenta]")
                add_directory(branch, full_path)
            else:
                size = os.path.getsize(full_path)
                tree.add(f"[bold green]{item}[/bold green] {size} bytes")

    add_directory(tree, path)
    console.print(tree)

@click.command()
def cli():
    current_path = os.getcwd()

    while True:
        command = console.input(f"[bold cyan]Current path: {current_path}[/bold cyan]\n"
                                "[bold cyan]Command ([/bold cyan][yellow]cd[/yellow] [bold cyan]path, [bold cyan][yellow]..[/yellow][bold cyan], [bold cyan][yellow]go[/yellow][bold cyan], [bold cyan][yellow]exit[/yellow][bold cyan]): [/bold cyan]")

        if command.startswith("cd "):
            new_path = command[3:].strip()
            if os.path.isdir(new_path):
                current_path = new_path
                console.print(f"[bold green]Changed directory to {current_path}[/bold green]")
            else:
                console.print(f"[bold red]Error:[/bold red] '{new_path}' is not a valid directory")
        elif command == "..":
            parent_path = os.path.dirname(current_path)
            if os.path.isdir(parent_path):
                current_path = parent_path
                console.print(f"[bold green]Changed directory to {current_path}[/bold green]")
            else:
                console.print(f"[bold red]Error:[/bold red] '{parent_path}' is not a valid directory")
        elif command == "go":
            display_directory_tree(current_path)
        elif command == "exit":
            console.print("[bold cyan]Exiting...[/bold cyan]")
            break
        else:
            console.print("[bold red]Invalid command.[/bold red] Please use 'cd <path>', '..', 'go', or 'exit' to exit.")

if __name__ == '__main__':
    cli()
