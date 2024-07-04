import os
import click
from rich.console import Console
from rich.tree import Tree

console = Console()

def format_size(size):
    """Return size in bytes, KB, and MB if size is greater than 0."""
    if size == 0:
        return ""
    kb_size = size / 1024
    mb_size = kb_size / 1024
    parts = [f"{size} bytes"]
    if kb_size >= 1:
        parts.append(f"{kb_size:.2f} KB")
    if mb_size >= 1:
        parts.append(f"{mb_size:.2f} MB")
    return " - ".join(parts)

def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fp = os.path.join(dirpath, filename)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def display_directory_tree(path):
    dir_size = get_directory_size(path)
    size_str = format_size(dir_size)
    tree = Tree(f"{path} {f'({size_str})' if size_str else ''}", guide_style="bold bright_blue")

    def add_directory(tree, path):
        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dir_size = get_directory_size(full_path)
                size_str = format_size(dir_size)
                branch = tree.add(f"[bold magenta]{item}/[/bold magenta] {f'({size_str})' if size_str else ''}")
                add_directory(branch, full_path)
            else:
                size = os.path.getsize(full_path)
                size_str = format_size(size)
                tree.add(f"[bold green]{item}[/bold green] {f'({size_str})' if size_str else ''}")

    add_directory(tree, path)
    console.print(tree)

@click.command()
def cli():
    current_path = os.getcwd()

    while True:
        command = console.input(f"[bold cyan]Current path: {current_path}[/bold cyan]\n"
                                "[bold cyan]Command ([/bold cyan][yellow]cd[/yellow] [bold cyan]path, [bold cyan][yellow]..[/yellow][bold cyan], [bold cyan][yellow]go[/yellow][bold cyan], [bold cyan][yellow]cls[/yellow][bold cyan], [bold cyan][yellow]exit[/yellow][bold cyan]): [/bold cyan]")

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
        elif command == "cls":
            console.clear()
        elif command == "exit":
            console.print("[bold cyan]Exiting...[/bold cyan]")
            break
        else:
            console.print("[bold red]Invalid command.[/bold red] Please use 'cd <path>', '..', 'go', 'cls', or 'exit' to exit.")

if __name__ == '__main__':
    cli()
