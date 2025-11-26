from src.utils.download import download_to_raw

# dataset available at: https://geoportal.statistics.gov.uk/datasets/c4f84c38814d4b82aa4760ade686c3cc/about


# NEEDS Fixing! Utility function needs extending to work for zip files!

if __name__ == '__main__':
    download_from_url = 'https://opendata.westofengland-ca.gov.uk/api/explore/v2.1/catalog/datasets/lep_lsoa_geog/exports/csv?lang=en&qv1=(bristol)&timezone=Europe%2FLondon&use_labels=true&delimiter=%2C'
    file_path = download_to_raw(download_url,'admin_codes_raw')