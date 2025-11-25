import polars as pl
from pathlib import Path

# available at: https://opendata.bristol.gov.uk/datasets/7d0994dded2348d5aff6d419b0c76bb9_0/explore

def get_root():
    '''returns project root'''

    # directory for this script
    SCRIPT_DIR = Path(__file__).resolve().parent

    # go up into project root
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    return PROJECT_ROOT# read in dataset from respective path


def clean_data(data, filter_codes):

    # rename columns and handle unwanted features
    new_cols = ['lsoa_code',
                'total_homes',
                'owned_homes',
                'owned_homes_outright',
                'owned_homes_shared_or_mortgaged',
                'rented_homes',
                'socially_rented_homes',
                'free_or_privately_rented']

    drop_cols = [str(x) for x in range(len(data.columns) - len(new_cols) - 1)]

    data = data.rename(dict(zip(data.columns,  new_cols + drop_cols + ['pct_rented'])))
    data = data.drop(drop_cols)

    # join is performed to check for any missing lsoa codes through null value creation
    data = filter_codes.select('lsoa_code').join(
        data,
        on='lsoa_code',
        how='left'
    )

    return data



if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    housing_tenure = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'nomis-tenure-ods.csv')
    bristol_lso_codes = pl.read_csv(PROJECT_ROOT / 'datasets' / 'processed' / 'bristol_admin_codes.csv')

    # clean the dataset
    housing_tenure = clean_data(housing_tenure, bristol_lso_codes)

    # save dataset
    save_file = PROJECT_ROOT / 'datasets' / 'processed' / 'housing_tenure.csv'
    housing_tenure.write_csv(save_file)