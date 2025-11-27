import polars as pl
from src.utils.paths import RAW_DIR, LOOKUP_DIR, PROCESSED_DIR
# available at: https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateepcbandcoraboveenglandandwales


def clean_data(data, filter_codes):

    # columns are dropped by index as column names are very long in the spreadsheet
    drop_columns = [data.columns[i] for i in [0, 1, 3]]
    data = data.drop(drop_columns)

    # rename column headers
    data = data.rename(dict(zip(data.columns,['msoa_code', 'epc_above_c_pct'])))

    data = filter_codes.select(['lsoa_code',
                                'msoa_code']).join(
        data,
        on='msoa_code',
        how='left'
    ).drop('msoa_code')

    return data

if __name__ == '__main__':
    # read in datasets
    epc_rating = pl.read_excel(RAW_DIR / 'epc_rating_raw.xlsx',
                                sheet_name='3a',
                                read_options={'skip_rows': 4})
    bristol_lso_codes = pl.read_csv(LOOKUP_DIR / 'bristol_admin_codes.csv')

    # clean the dataset
    epc_rating = clean_data(epc_rating, bristol_lso_codes)

    # save dataset
    save_file = PROCESSED_DIR / 'epc_rating.csv'
    epc_rating.write_csv(save_file)