import polars as pl
from src.utils.paths import RAW_DIR, PROCESSED_DIR, LOOKUP_DIR, PROJECT_ROOT


# available at: https://www.ons.gov.uk/datasets/TS045/editions/2021/versions/4/filter-outputs/c890d032-97e0-4c9e-8f8a-814e619e2d50#get-data


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
    vehicle_availability = pl.read_csv(RAW_DIR / 'car_van_availability_raw.csv')
    bristol_lso_codes = pl.read_csv(LOOKUP_DIR / 'lsoa_lookup.csv')

    # clean the dataset
    vehicle_availability = clean_data(vehicle_availability, bristol_lso_codes)

    # save dataset
    save_file = PROCESSED_DIR / 'car_van_availability.csv'
    vehicle_availability.write_csv(save_file)