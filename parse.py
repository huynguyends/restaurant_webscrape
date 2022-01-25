import re
import requests
import pickle
from bs4 import BeautifulSoup
import codecs
import time
import json



def parse_all_pages():
    item_list = []

    # reading scraped html files from local storage
    dir_name = "scraped_html" 
    for page in os.listdir(dir_name):
    file_path = os.path.join(dir_name,page)
    print("reading " + file_path)

    def parse_one_item(venue_list_item):
        item_dict = {}

        item_dict['name'] = venue_list_item.h4.text
        item_dict['address'] = venue_list_item.find_all('p')[0].text.replace('\n', ' ').strip()
        item_dict['phone'] = venue_list_item.find_all('p')[1].text.replace('\n', ' ').strip()
        item_dict['open_hours'] = venue_list_item.find_all('p')[2].text.replace('\n', ' ').strip()
        # if item for restaurant will have cuisine, shop won't have, so just store None
        item_dict['cuisine'] = venue_list_item.find_all('p')[3].text.replace('\n', ' ').strip() if 'Cuisine' in venue_list_item.find_all('p')[3].text else 'N/A'
        item_dict['description'] = venue_list_item.find_all('p')[-1].text.replace('\n', ' ').strip()

        return item_dict


    def parse_all_items_one_page(soup, item_list):
        venue_list_items = soup.findAll('div',{'class':re.compile(r"^venue-list-item")})
        for venue_list_item in venue_list_items:
            item_parsed = parse_one_item(venue_list_item)
            print(item_parsed)
            # print(len(item_list))
            item_list.append(item_parsed)

        return item_list    


    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        item_list = parse_all_items_one_page(soup, item_list)

    # save json 
    f = open(os.path.join('parsed_json','items_list.json'), 'w')
    f.write(json.dumps(item_list, indent=2))
    f.close()

    return item_list


if __name__ == '__main__':
    parse_all_pages()