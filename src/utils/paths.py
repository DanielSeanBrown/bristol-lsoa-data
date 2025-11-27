from pathlib import Path

# directory for this file
THIS_FILE = Path(__file__).resolve()

# project root (that being two levels up from here)
PROJECT_ROOT = THIS_FILE.parents[2]

# data directories
DATASETS_DIR = PROJECT_ROOT / 'datasets'
LOOKUP_DIR = DATASETS_DIR / 'lookup'
RAW_DIR = DATASETS_DIR / 'raw'
PROCESSED_DIR = DATASETS_DIR / 'processed'
