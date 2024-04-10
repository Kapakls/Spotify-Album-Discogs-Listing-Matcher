from bs4 import BeautifulSoup
from pathlib import Path
import cloudscraper
import json
import os
import re
import pycountry
import subprocess

def clean_filename(filename):
    clean_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return clean_filename


def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path) as json_file:
            return json.load(json_file)
    return {}


def save_listing_data(data_list, artist_name, album_name, output):
    artist_name_clean = clean_filename(artist_name)
    album_name_clean = clean_filename(album_name)
    full_path = os.path.join(output, f"{artist_name_clean} - {album_name_clean}.json")

    if not os.path.exists(output):
        os.makedirs(output)

    if not os.path.exists(full_path):
        with open(full_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_list, json_file, indent=2)
    print(f'Debug - Data extracted and saved to {artist_name} - {album_name}.json')


def extract_data_and_save(album, output, scraper):
    album_name = album['album']['name']
    artists = album['album']['artists']

    for artist in artists:
        artist_name = artist['name']
      
        limit = 100  
        total_pages = 5

        for page in range(1, total_pages + 1):
            URL_search_code = f"{artist_name.replace(' ', '+')}+{album_name.replace(' ', '+')}&page={page}&per_page={limit}"
            URL = f'https://www.discogs.com/sell/list?q={URL_search_code}'
            print('Debug - Extraction URL:', URL)

            response = scraper.get(URL)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                listings = soup.find_all('tr', class_=['shortcut_navigable', 'shortcut_navigable unavailable'])
            else:
                continue

            data_list = []

            for item in listings:
                listing_data = {}
                listing_data['title'] = item.select_one('.item_description_title').get_text(strip=True)
                album_cover = album['album'].get('images', [{}])[0].get('url', 'N/A')
                listing_data['cover'] = album_cover
                ships_from_element = item.select_one('.seller_info li:-soup-contains("Ships From:")')
                seller_location_text = ships_from_element.get_text(strip=True).replace('Ships From:', '') if ships_from_element else 'N/A'

                try:
                    seller_location_iso = pycountry.countries.get(name=seller_location_text).alpha_2
                except AttributeError:
                    seller_location_iso = 'N/A'

                listing_data['seller_location'] = seller_location_iso
                listing_url_element = item.select_one('.item_description_title[href]')
                listing_data['listing_url'] = f'https://www.discogs.com{listing_url_element["href"]}' if listing_url_element else 'N/A'

                data_list.append(listing_data)

            save_listing_data(data_list, artist_name, album_name, output)


def main():

    scraper = cloudscraper.create_scraper()
    
    main_path = Path(__file__).resolve().parent
    albums_path = os.path.join(main_path, 'Data', 'Spotify json Data', 'albums.json')

    albums = load_json(albums_path)     

    output = os.path.join(main_path, 'Data', 'Discogs json Data')
    if not os.path.exists(output):
        os.makedirs(output)
    
    filter = os.path.join(main_path, 'filter.py')

    for album in albums.get('items', []):
        extract_data_and_save(album, output, scraper)

    subprocess.run(['python', filter])

if __name__ == "__main__":
    main()
