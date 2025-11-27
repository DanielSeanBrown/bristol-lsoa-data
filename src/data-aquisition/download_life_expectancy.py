from src.utils.download import download_from_url

# dataset available at: https://opendata.bristol.gov.uk/datasets/d51a84ba68234432b9108491844b1e23_19/explore

if __name__ == '__main__':
    download_url = 'https://hub.arcgis.com/api/v3/datasets/d51a84ba68234432b9108491844b1e23_19/downloads/data?format=csv&spatialRefId=27700&where=1%3D1'
    file_path = download_from_url(download_url,'life_expectancy_raw.csv')