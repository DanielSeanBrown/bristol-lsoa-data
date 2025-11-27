import polars as pl

from src.utils.paths import RAW_DIR, LOOKUP_DIR, PROCESSED_DIR


# available at: https://opendata.westofengland-ca.gov.uk/explore/dataset/nomis-tenure-ods/export/?disjunctive.ladnm&refine.ladnm=Bristol,+City+of

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
    housing_tenure = pl.read_csv(RAW_DIR /  'housing_tenure_raw.csv')
    bristol_lso_codes = pl.read_csv(LOOKUP_DIR / 'lsoa_lookup.csv')

    # clean the dataset
    housing_tenure = clean_data(housing_tenure, bristol_lso_codes)

    # save dataset
    save_file = PROCESSED_DIR / 'housing_tenure.csv'
    housing_tenure.write_csv(save_file)