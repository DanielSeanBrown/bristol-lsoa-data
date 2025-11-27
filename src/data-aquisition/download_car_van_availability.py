from src.utils.download import download_from_url

# available at: https://www.ons.gov.uk/datasets/TS045/editions/2021/versions/4

if __name__ == '__main__':
    download_url = 'https://static.ons.gov.uk/datasets/TS045-2021-4.csv'
    file_path = download_from_url(download_url,'car_van_availability_raw.csv')

