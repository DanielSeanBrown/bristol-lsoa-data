import polars as pl
from pathlib import Path

# available at: https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateepcbandcoraboveenglandandwales


def clean_data(data, filter_codes):
    pass

if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    depivation_index = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'Indices_of_Deprivation_2025.csv')
    print(depivation_index.head())
