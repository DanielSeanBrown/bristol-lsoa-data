import polars as pl
from src.utils.paths import RAW_DIR, PROCESSED_DIR, LOOKUP_DIR

def perform_celaning(dataset, code_lookup):
    # remove irrelevant columns
    dataset = dataset.drop(['OBJECTID',
                            'WARD_NAME',
                            'LIFE_EXPECTANCY_YEARS_LCL',
                            'LIFE_EXPECTANCY_YEARS_UCL'])

    # standardise date column for single year value
    dataset = dataset.with_columns(
        pl.col('PERIOD').str.split('-').list.get(0)
    )

    # rename column names to follow conventions
    dataset = dataset.rename({col: col.lower() for col in dataset.columns})
    dataset = dataset.rename({'period':'year'})

    # perform join to assign lsoa codes based on ward codes
    dataset = code_lookup.select(['lsoa_code', 'ward_code']).join(
        dataset,
        on='ward_code',
        how='left'
    )

    return dataset



if __name__ == '__main__':
    # read in datasets
    life_expectancy = pl.read_csv(RAW_DIR /  'life_expectancy_raw.csv')
    lsoa_lookup = pl.read_csv(LOOKUP_DIR / 'lsoa_lookup.csv')

    # perform data cleaning
    life_expectancy = perform_celaning(life_expectancy, lsoa_lookup)

    # save dataset
    save_file = PROCESSED_DIR / 'life_expectancy.csv'
    life_expectancy.write_csv(save_file)