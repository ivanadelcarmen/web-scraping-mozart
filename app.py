import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def create_catalogue(url: str, html_object: str) -> list:
    """
    Function:
    Scrapes the requested URL and creates arrays with each work's information from the catalogue.

    Args:
    url (str): The requested URL.
    html_object (str): The type of HTML objects to fetch.

    Returns:
    list: A list containing lists with each work's details in order.
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    data_cells = soup.find_all(html_object)

    # Fetch row-wise each detail based on the first letter of each HTML object's unique identifier
    numbers = [cell.getText().strip() for cell in data_cells if cell.get('data-cell-id').startswith('B')]
    titles = [cell.getText().strip() for cell in data_cells if cell.get('data-cell-id').startswith('C')]

    keys = []
    for cell in data_cells:
        if cell.get('data-cell-id').startswith('D'):
            key = cell.getText().strip()
            keys.append(key) if key else keys.append('N/A') # Replace blank values with 'N/A'
    
    locations = [cell.getText().strip() for cell in data_cells if cell.get('data-cell-id').startswith('F')]
    years = [cell.getText().strip() for cell in data_cells if cell.get('data-cell-id').startswith('E')]

    genres = [re.findall(r'(?<=\s).*$', cell.getText().strip())[0] # Filter from each work's genre the text without initials, signs or numbers
              for cell in data_cells if cell.get('data-cell-id').startswith('G')]

    # Use enumerate() with one of the lists ('numbers' in this case) to create an index parameter for the other ones
    catalogue = [[item, titles[idx], keys[idx], locations[idx], years[idx], genres[idx]] for idx, item in enumerate(numbers)]
  
    return catalogue


if __name__ == '__main__':
    url = 'https://allaboutmozart.com/mozart-kochel-catalogue-works-compositions-koechel/'
    catalogue = create_catalogue(url, 'td')
    sorted_catalogue = sorted(catalogue, key=lambda x: (x[0], x[4])) # Sort rows by number and year

    # Build the DataFrame using the sorted catalogue and a specified header
    header = ['number', 'title', 'key', 'location', 'year', 'genre']
    df = pd.DataFrame(sorted_catalogue, columns=header)
    df['count_per_genre'] = df.groupby('genre')['number'].transform('count') # Include in each row the count of works per its genre
    
    # Write the DataFrame to the .csv file
    file_name = 'catalogue.csv'
    df.to_csv(file_name, index=False)
