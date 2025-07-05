from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from src.scraper import Scraper
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os

console = Console()

def download_task(scraper, image, name):
    try:
        scraper.download_image(image)
        return (image, None)  # success
    except Exception as e:
        return (image, e)     # failed

def download_images_multithreaded(scraper, images, name, max_workers=8):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]Downloading images for {name}[/cyan]", total=len(images))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(download_task, scraper, image, name) for image in images]

            for future in as_completed(futures):
                image, error = future.result()
                progress.update(task, advance=1)

                if error:
                    console.print(f"[red]Failed to download: {image.get('FILENAME')} — {error}[/red]")

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

    download_images_multithreaded(scraper, images, name, max_workers=8)


