from src.utils.download import download_from_url

# dataset available at: https://www.ons.gov.uk/peoplepopulationandcommunity/educationandchildcare/datasets/childcareaccessibilityinenglanddata

if __name__ == '__main__':
    download_url = 'https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/educationandchildcare/datasets/childcareaccessibilityinenglanddata/2023/childcareaccessibilityinengland.xlsx'
    file_path = download_from_url(download_url,'childcare_accessibility_raw.xlsx')

