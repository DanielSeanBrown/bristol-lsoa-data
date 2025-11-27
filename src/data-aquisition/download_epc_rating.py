from src.utils.download import download_from_url

# dataset available at: https://www.ons.gov.uk/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateepcbandcoraboveenglandandwales

if __name__ == '__main__':
    download_url = 'https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/housing/datasets/energyperformancecertificateepcbandcoraboveenglandandwales/march2025/epcbandcoraboveenglandandwales.xlsx'
    file_path = download_from_url(download_url,'epc_rating_raw.xlsx')