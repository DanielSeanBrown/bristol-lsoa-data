import requests
from pathlib import Path
from src.utils.paths import RAW_DIR

def download_to_raw(url: str, filename: str):
    '''Download a file from a URL and save it to datasets/raw'''

    filepath = RAW_DIR / filename

    response = requests.get(url)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"Saved: {filepath}")
    return filepath
