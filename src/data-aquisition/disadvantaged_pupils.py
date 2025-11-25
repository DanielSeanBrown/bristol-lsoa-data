import polars as pl
from pathlib import Path

# available at: https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateepcbandcoraboveenglandandwales

def get_root():
    '''returns project root'''

    # directory for this script
    SCRIPT_DIR = Path(__file__).resolve().parent

    # go up into project root
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    return PROJECT_ROOT# read in dataset from respective path

def clean_data(data, filter_codes):
    # rename column headers
    data = data.rename(dict(zip(data.columns,['index',
                                              'ward_code',
                                              'ward_name',
                                              'year',
                                              'disadvantaged_num',
                                              'disadvantaged_pct'])))
    print(data.head())
    data = filter_codes.select(['lsoa_code',
                                'ward_code']).join(
        data,
        on='ward_code',
        how='left'
    ).drop(['ward_code','ward_name','index'])

    return data

if __name__ == '__main__':
    # read in datasets
    PROJECT_ROOT = get_root()
    disadvantaged_pupils = pl.read_csv(PROJECT_ROOT / 'datasets' / 'raw' / 'Pupils_classed_as_disadvantaged_in_Bristol_by_Ward.csv')
    bristol_lso_codes = pl.read_csv(PROJECT_ROOT / 'datasets' / 'processed' / 'bristol_admin_codes.csv')

    # clean the dataset
    disadvantaged_pupils = clean_data(disadvantaged_pupils, bristol_lso_codes)

    # save dataset
    save_file = PROJECT_ROOT / 'datasets' / 'processed' / 'disadvantaged_pupils.csv'
    disadvantaged_pupils.write_csv(save_file)