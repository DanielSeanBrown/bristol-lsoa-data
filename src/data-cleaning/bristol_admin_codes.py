import polars as pl
from src.utils.paths import RAW_DIR, LOOKUP_DIR



def create_lsoa_lookup(dataset):

    # filter out columns not related to administrative codes
    lsoa_lookup = dataset.select(['LSOA Code',
                                  'MSOA Code',
                                  'Ward code 2024',
                                  'Local Authority Code'])

    # rename column names to follow naming conventions
    lsoa_lookup = (
        lsoa_lookup
        .rename({
            'LSOA Code': 'lsoa_code',
            'MSOA Code': 'msoa_code',
            'Ward code 2024': 'ward_code',
            'Local Authority Code': 'local_authority_code',
        })
        .filter(pl.col('local_authority_code') == 'E06000023')
    )

    return lsoa_lookup


def create_georgraphy_lookup(dataset):
    # filter out columns not related to administrative codes
    geography_lookup = dataset.select(['Geo Point',
                                       'Geo Shape',
                                       'LSOA Code',
                                       'Easting',
                                       'Northing',
                                       'Longitude',
                                       'Latitude',
                                       'Local Authority Code'])

    # rename column names to follow naming conventions
    geography_lookup = (
        geography_lookup
        .rename({
            'Geo Point': 'geo_point',
            'Geo Shape': 'geo_shape',
            'LSOA Code': 'lsoa_code',
            'Easting': 'easting',
            'Northing': 'northing',
            'Longitude': 'longitude',
            'Latitude': 'latitude',
            'Local Authority Code': 'local_authority_code'
        })
        .filter(pl.col('local_authority_code') == 'E06000023')
    )

    return geography_lookup

if __name__ == '__main__':
    # read in raw dataset
    admin_codes_raw = pl.read_csv(RAW_DIR / 'admin_codes_raw.csv')

    # create and save dataset 1
    lsoa_lookup = create_lsoa_lookup(admin_codes_raw)
    lsoa_lookup.write_csv(LOOKUP_DIR / 'lsoa_lookup.csv')

    # create and save dataset 2
    geography_lookup = create_georgraphy_lookup(admin_codes_raw)
    geography_lookup.write_csv(LOOKUP_DIR / 'geography_lookup.csv')