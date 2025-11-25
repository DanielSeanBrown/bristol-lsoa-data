import polars as pl
from pathlib import Path

# available at: https://www.ons.gov.uk/peoplepopulationandcommunity/educationandchildcare/datasets/childcareaccessibilityinenglanddata

# Taken from excel source file
'''Childcare accessibility is a ratio of childcare places to number of children aged 7 and under in each administrative boundary.
To calculate the equivalent accessible childcare places per 100 children, multiply the ratio by 100.
Childcare accessibility ratios are produced individually for driving and public transport modes.
A weighted average of these, based on car ownership in administrative boundaries (Census 2021), is used to produce the childcare accessibility. '''


def get_root():
    '''returns project root'''

    # directory for this script
    SCRIPT_DIR = Path(__file__).resolve().parent

    # go up into project root
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    return PROJECT_ROOT

def clean_data(data, filter_codes):
    original_column_names = data.columns
    new_column_names = ['lsoa_code',
                        'ca',
                        'ca_driving_only',
                        'ca_public_transport_only',
                        'ca_good_or_outstanding',
                        'ca_good_or_outstanding_driving_only',
                        'ca_good_or_outstanding_public_transport_only']
    data = data.rename(dict(zip(original_column_names, new_column_names)))
    data = filter_codes.select('lsoa_code').join(
        data,
        on='lsoa_code',
        how='left'
    )

    return data

if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    bristol_admin_codes = pl.read_csv(PROJECT_ROOT / 'datasets' / 'processed' / 'bristol_admin_codes.csv')
    cc_accessibility = pl.read_excel(PROJECT_ROOT / 'datasets' / 'raw' / 'childcareaccessibilityinengland.xlsx',
                                     sheet_name='Table_2',
                                     read_options={'skip_rows': 6})

    # clean data
    cc_accessibility = clean_data(cc_accessibility, bristol_admin_codes)

    # save dataset
    save_file = PROJECT_ROOT / 'datasets' / 'processed' / 'childcare_accessibility.csv'
    cc_accessibility.write_csv(save_file)