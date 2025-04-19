import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def create_catalogue(url: str, html_object: str) -> list:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    data_cells = soup.find_all(html_object)

    numbers = [cell.getText().strip() for cell in data_cells if cell.get('data-cell-id').startswith('B')]
    titles = [cell.getText().strip() for cell in data_cells if cell.get('data-cell-id').startswith('C')]

    keys = []
    for cell in data_cells:
        if cell.get('data-cell-id').startswith('D'):
            key = cell.getText().strip()
            keys.append(key) if key else keys.append('N/A')
    
    locations = [cell.getText().strip() for cell in data_cells if cell.get('data-cell-id').startswith('F')]
    years = [int(cell.getText()) for cell in data_cells if cell.get('data-cell-id').startswith('E')]
    genres = [re.findall(r'(?<=\s).*$', cell.getText().strip())[0] for cell in data_cells if cell.get('data-cell-id').startswith('G')]

    # Use the enumerate() generator with one of the lists ('numbers' in this case) to create an index parameter for the other ones
    catalogue = [[item, titles[idx], keys[idx], locations[idx], years[idx], genres[idx]] for idx, item in enumerate(numbers)]
  
    return catalogue


if __name__ == '__main__':
    url = 'https://allaboutmozart.com/mozart-kochel-catalogue-works-compositions-koechel/'
    catalogue = create_catalogue(url, 'td')
    sorted_catalogue = sorted(catalogue, key=lambda x: (x[0], x[4])) # Sort by number and year

    file_name = 'catalogue.csv'
    header = ['number', 'title', 'key', 'location', 'year', 'genre']
    df = pd.DataFrame(sorted_catalogue, columns=header)
    df.to_csv(file_name, index=False)
