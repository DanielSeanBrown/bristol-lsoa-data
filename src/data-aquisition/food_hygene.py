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

    # filter out unuseful columns
    data = data.select(['POSTCODE',
                        'RATING_DATE',
                        'RATING',])

    # rename column names to follow naming conventions
    data = data.rename(mapping=({'POSTCODE': 'postcode',
                                 'RATING_DATE': 'rating_date',
                                 'RATING': 'rating'}))

    # drop nulls
    data = data.drop_nulls()

    # ensure consistent postcode formatting
    data = clean_postcode(data)

    # convert string with date time info to just date
    data = data.with_columns(pl.col("rating_date").str.strptime(pl.Date,"%Y/%m/%d %T %#z"))

    # join on postcodes to allocate lsoa codes
    data = data.join(other=filter_codes.select(['lsoa_code','postcode']),on='postcode', how='left')

    return data

def clean_postcode(dataset):
    # remove whitespace and uppercase
    dataset = dataset.with_columns(
        pl.col("postcode")
        .str.replace_all(r"\s+", "")
        .str.to_uppercase()  # u
    )

    # split start and end of postcode
    dataset = dataset.with_columns([
        pl.col("postcode").str.head(-3).alias("outward"),  # everything except last 3 chars
        pl.col("postcode").str.tail(3).alias("inward")  # last 3 chars
    ])

    # combine to ensure only single space
    dataset = dataset.with_columns(
        (pl.col("outward") + " " + pl.col("inward")).alias("postcode")
    ).drop(["outward", "inward"])

    return dataset


if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    food_hygene = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'Food_Hygiene_Ratings.csv')
    bristol_lso_codes = pl.read_csv(PROJECT_ROOT / 'datasets' / 'processed' / 'bristol_postcodes.csv')

    # clean the dataset
    food_hygene = clean_data(food_hygene, bristol_lso_codes)

    # save dataset
    save_file = PROJECT_ROOT / 'datasets' / 'processed' / 'food_hygene.csv'
    food_hygene.write_csv(save_file)