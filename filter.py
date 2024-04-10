from pathlib import Path
import json
import os

def jaccard_similarity(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0


def load_listing_data(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)


def calculate_similarity(json_list_clear, title_list_clear):
    return jaccard_similarity(json_list_clear, title_list_clear)


def filter_matching_listings(item, similarity_threshold):
    matching_listings = []

    json_name_without_extension = os.path.splitext(item['json_file_name'])[0]
    json_list = json_name_without_extension.split()
    json_list_clear = [element for element in json_list if '-' not in element]

    for subitem in item['listing_data']:
        title_list = subitem.get('title', '').split()
        title_list_clear = [element for element in title_list if '-' not in element]

        similarity = calculate_similarity(json_list_clear, title_list_clear)

        if similarity >= similarity_threshold:
            subitem_info = {
                'listing_URL': subitem.get('listing_url'),
                'cover': subitem.get('cover'),
                'region': subitem.get('seller_location')
            }
            matching_listings.append(subitem_info)

    return matching_listings


def main(input_directory, output_directory, similarity_threshold):

    json_files = [f for f in os.listdir(input_directory) if f.endswith('.json')]

    for json_file_name in json_files:
        json_file_path = os.path.join(input_directory, json_file_name)
        listing_data = load_listing_data(json_file_path)
        
        result = filter_matching_listings({'json_file_name': json_file_name, 'listing_data': listing_data}, similarity_threshold)

        if len(result) > 0:
            output_file_path = os.path.join(output_directory, f"{json_file_name}.json")
            os.makedirs(output_directory, exist_ok=True)
                
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(result, output_file, indent=2)
                
            print('Debug - Matching listings saved to:', output_file_path)


if __name__ == "__main__":
    similarity_threshold = 0.1

    main_path = Path(__file__).resolve().parent

    input_directory = os.path.join(main_path, 'Data', 'Discogs json Data')
    output_directory = os.path.join(main_path, 'Data', 'Matching Listings')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    main(input_directory, output_directory, similarity_threshold)
