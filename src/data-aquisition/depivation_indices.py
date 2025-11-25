import polars as pl
from pathlib import Path

# available at: https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateepcbandcoraboveenglandandwales

def get_root():
    '''returns project root'''

    # directory for this script
    SCRIPT_DIR = Path(__file__).resolve().parent

    # go up into project root
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    return PROJECT_ROOT# read in dataset from respective path

def clean_data(data, filter_codes):
    pass

if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    depivation_index = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'Indices_of_Deprivation_2025.csv')
    print(depivation_index.head())
