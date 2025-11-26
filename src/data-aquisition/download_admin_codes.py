from src.utils.download import download_from_url

# datasets available at: https://opendata.westofengland-ca.gov.uk/explore/dataset/lep_lsoa_geog/map/?sort=lsoa21nm&q=bristol&location=14,51.4547,-2.57677&basemap=jawg.streets

if __name__ == '__main__':
    download_url = 'https://opendata.westofengland-ca.gov.uk/api/explore/v2.1/catalog/datasets/lep_lsoa_geog/exports/csv?lang=en&qv1=(bristol)&timezone=Europe%2FLondon&use_labels=true&delimiter=%2C'
    file_path = download_from_url(download_url,'admin_codes_raw.csv')