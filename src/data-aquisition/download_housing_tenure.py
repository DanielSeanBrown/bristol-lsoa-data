from src.utils.download import download_from_url

# available at: https://opendata.westofengland-ca.gov.uk/explore/dataset/nomis-tenure-ods/export/?disjunctive.ladnm&refine.ladnm=Bristol,+City+of

if __name__ == '__main__':
    download_url = 'https://opendata.westofengland-ca.gov.uk/api/explore/v2.1/catalog/datasets/nomis-tenure-ods/exports/csv?lang=en&refine=ladnm%3A%22Bristol%2C%20City%20of%22&facet=facet(name%3D%22ladnm%22%2C%20disjunctive%3Dtrue)&timezone=Europe%2FLondon&use_labels=true&delimiter=%2C'
    file_path = download_from_url(download_url,'housing_tenure_raw.csv')