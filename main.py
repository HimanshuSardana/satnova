from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from src.scraper import Scraper
import json
import os

console = Console()

with open('./constants/locations.json', 'r') as f:
    data = json.load(f)['locations']

for location in data:
    name = location['name']
    console.rule(f"[bold blue]{name}[/bold blue]")
    scraper = Scraper(name)

    images = scraper.get_images()

    if not images:
        console.print(f"[yellow]No images found for {name}[/yellow]")
        continue

    console.print(Panel(f"[green]Found {len(images)} images for [bold]{name}[/bold]"))

    os.makedirs(f"images/{name}", exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]Downloading images for {name}[/cyan]", total=len(images))

        for image in images:
            try:
                scraper.download_image(image)
                progress.update(task, advance=1)
            except Exception as e:
                console.print(f"[red]Failed to download: {image.get('FILENAME')} — {e}[/red]")

