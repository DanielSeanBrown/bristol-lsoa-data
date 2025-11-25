from pathlib import Path

# directory for this file
THIS_FILE = Path(__file__).resolve()

# project root (that being two levels up from here)
PROJECT_ROOT = THIS_FILE.parents[2]

# data directories
DATSETS_DIR = PROJECT_ROOT / "datasets"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
