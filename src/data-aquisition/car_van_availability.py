import polars as pl
from pathlib import Path

# available at: https://www.ons.gov.uk/datasets/TS045/editions/2021/versions/4/filter-outputs/c890d032-97e0-4c9e-8f8a-814e619e2d50#get-data

def get_root():
    '''returns project root'''

    # directory for this script
    SCRIPT_DIR = Path(__file__).resolve().parent

    # go up into project root
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    return PROJECT_ROOT# read in dataset from respective path

def clean_data(data, filter_codes):
    # rename columns
    new_column_names = ['lsoa_code',
                        'lsoa_name',
                        'cva_code',
                        'cva_name',
                        'observed']
    data = data.rename(dict(zip(data.columns, new_column_names)))

    # perform join to assign lsoa codes based on lsoa codes
    data = filter_codes.select('lsoa_code').join(
        data,
        on='lsoa_code',
        how='left'
    ).drop('lsoa_name')

    return data

if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    vehicle_availability = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'TS045-2021-4-filtered-2025-11-24T13_51_04Z.csv')
    bristol_lso_codes = pl.read_csv(PROJECT_ROOT / 'datasets' / 'processed' / 'bristol_admin_codes.csv')

    # clean the dataset
    vehicle_availability = clean_data(vehicle_availability, bristol_lso_codes)

    # save dataset
    save_file = PROJECT_ROOT / 'datasets' / 'processed' / 'vehicle_availability.csv'
    vehicle_availability.write_csv(save_file)