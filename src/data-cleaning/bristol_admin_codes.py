import polars as pl
from src.utils.paths import RAW_DIR, LOOKUP_DIR


def clean_data(dataset):

    # filter out columns related to administrative codes
    admin_codes = dataset.select(['LSOA Code',
                                  'MSOA Code',
                                  'Ward code 2024',
                                  'Local Authority Code'])

    # rename column names to follow naming conventions
    bristol_admin_codes = (
        admin_codes
        .rename({
            'LSOA Code': 'lsoa_code',
            'MSOA Code': 'msoa_code',
            'Ward code 2024': 'ward_code',
            'Local Authority Code': 'local_authority_code',
        })
        .filter(pl.col('local_authority_code') == 'E06000023')
    )


    return bristol_admin_codes

if __name__ == '__main__':
    # read in raw dataset
    admin_codes_raw = pl.read_csv(RAW_DIR / 'admin_codes_raw.csv')

    # clean datasets and save
    bristol_admin_codes = clean_data(admin_codes_raw)
    bristol_admin_codes.write_csv(LOOKUP_DIR / 'bristol_admin_codes.csv')