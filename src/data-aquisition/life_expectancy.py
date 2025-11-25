import polars as pl
from pathlib import Path

# available at: https://opendata.bristol.gov.uk/datasets/d51a84ba68234432b9108491844b1e23_19/explore

def get_root():
    '''returns project root'''

    # directory for this script
    SCRIPT_DIR = Path(__file__).resolve().parent

    # go up into project root
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    return PROJECT_ROOT

def perform_celaning(life_expectancy_at_birth, bristol_lso_codes):
    # remove irrelevant columns
    life_expectancy_at_birth = life_expectancy_at_birth.drop(['OBJECTID',
                                                              'WARD_NAME',
                                                              'LIFE_EXPECTANCY_YEARS_LCL',
                                                              'LIFE_EXPECTANCY_YEARS_UCL'])

    # standardise date column for single year value
    life_expectancy_at_birth = life_expectancy_at_birth.with_columns(
        pl.col('PERIOD').str.split('-').list.get(0)
    )

    # rename column names to follow conventions
    life_expectancy_at_birth = life_expectancy_at_birth.rename({col: col.lower() for col in life_expectancy_at_birth.columns})
    life_expectancy_at_birth = life_expectancy_at_birth.rename({'period':'year'})

    # perform join to assign lsoa codes based on ward codes
    life_expectancy_data = bristol_lso_codes.select(['lsoa_code', 'ward_code']).join(
        life_expectancy_at_birth,
        on='ward_code',
        how='left'
    )

    return life_expectancy_data



if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    life_expectancy_at_birth = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'Life_Expectancy_at_birth_in_Bristol_by_Ward.csv')
    bristol_lso_codes = pl.read_csv(PROJECT_ROOT / 'datasets' / 'processed' / 'bristol_admin_codes.csv')

    # perform data cleaning
    life_expectancy = perform_celaning(life_expectancy_at_birth, bristol_lso_codes)

    # save dataset
    save_file = PROJECT_ROOT / 'datasets' / 'processed' / 'life_expectancy.csv'
    life_expectancy.write_csv(save_file)