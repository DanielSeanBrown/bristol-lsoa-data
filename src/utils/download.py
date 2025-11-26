import requests
from src.utils.paths import RAW_DIR
from pathlib import Path


def download_from_url(url: str, filename: str, output_dir: Path = RAW_DIR):
    '''Download a file from a URL and save it to datasets/raw'''

    filepath = output_dir / filename

    response = requests.get(url)
    response.raise_for_status()

    with open(filepath, 'wb') as f:
        f.write(response.content)

    print(f'Saved: {filepath}')
    return filepath