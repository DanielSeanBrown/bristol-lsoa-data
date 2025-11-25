import polars as pl
from pathlib import Path

# datasets available at: https://opendata.westofengland-ca.gov.uk/explore/dataset/lep_lsoa_geog/map/?sort=lsoa21nm&q=bristol&location=14,51.4547,-2.57677&basemap=jawg.streets
# and at: https://geoportal.statistics.gov.uk/datasets/c4f84c38814d4b82aa4760ade686c3cc/about

def get_root():
    '''returns project root'''

    # directory for this script
    SCRIPT_DIR = Path(__file__).resolve().parent

    # go up into project root
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    return PROJECT_ROOT

def clean_data(admin_codes, national_lookup_data):

    # filter out columns related to administrative codes
    admin_codes = admin_codes.select(['LSOA Code',
                                      'MSOA Code',
                                      'Ward code 2024',
                                      'Local Authority Code'])

    # rename column names to follow naming conventions
    admin_codes = admin_codes.rename(mapping=({'LSOA Code': 'lsoa_code',
                                               'MSOA Code': 'msoa_code',
                                               'Ward code 2024': 'ward_code',
                                               'Local Authority Code': 'local_authority_code'}))

    bristol_admin_codes = admin_codes.filter(pl.col('local_authority_code') == 'E06000023')


    # filter national lookup dataset to just postcodes and lsoa codes
    national_lookup_data = national_lookup_data.select(['pcds',
                                                        'lsoa21cd'])
    national_lookup_data = national_lookup_data.rename(mapping=({'pcds': 'postcode',
                                                                 'lsoa21cd': 'lsoa_code'}))

    # join on bristol lsoa codes to reduce national postcodes to just bristol
    bristol_admin_areas_postcodes = bristol_admin_codes.join(other=national_lookup_data,
                                                             on='lsoa_code',
                                                             how='left')

    return bristol_admin_codes, bristol_admin_areas_postcodes

if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    bristol_admin_data = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'lep_lsoa_geog.csv')
    national_lookup_data = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'PCD_OA21_LSOA21_MSOA21_LAD_NOV25_UK_LU.csv')

    # clean datasets
    bristol_admin_codes, bristol_postcodes = clean_data(bristol_admin_data, national_lookup_data)

    # save datasetS
    SAVE_DIR = PROJECT_ROOT / 'datasets' / 'processed'
    bristol_postcodes.write_csv(SAVE_DIR / 'bristol_postcodes.csv')
    bristol_admin_codes.write_csv(SAVE_DIR / 'bristol_admin_codes.csv')