import json
import os
import requests
from bs4 import BeautifulSoup

def parse_mfc_url(url) -> str:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if check_if_page_is_empty(soup):
            print(" EMPTY PAGE detected")
            return None

        
        if check_if_url_contains_li(soup):
            return None # NOT SUPPORTED YET
        else:
            captions_text = get_div_text_by_classname(soup, "page-caption")
            content_text = get_div_text_by_classname(soup, "content-block")
            return captions_text + content_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    # except Exception as e:
    #     print(f"An error occurred: {e}")


def check_if_url_contains_li(soup: BeautifulSoup) -> bool:
    return len(soup.find_all('div', class_="accordion")) > 0

def check_if_page_is_empty(soup: BeautifulSoup) -> bool:
    return len(soup.find('div', class_="page-caption").get_text(strip=True)) == 0
    
def get_div_text_by_classname(soup: BeautifulSoup, classname: str) -> str:
    class_encounters = soup.find_all('div', class_=classname)
    res_text = ""
    for content in class_encounters:
        res_text += content.get_text(strip=True)
        res_text += "\n\n"
    return res_text


RES_FOLDER = "results"

if __name__ == '__main__':
    for id in range(1, 1600):
        path_to_res_folder = os.path.join(RES_FOLDER, f"{id}")
        
        url_to_parse = f"https://mfc66.ru/services/item?id={id}"
        parse_result = parse_mfc_url(url_to_parse)
        if parse_result is None:
            print(f"Skipping {id}")
            continue
        parse_result = parse_result.replace(":", ": ") # add spaces after columns
        
        topic = parse_result.split("\n\n")[0]
        metadata = {"id": id, "topic": topic, "link": url_to_parse}
        
        metadata_path = os.path.join(path_to_res_folder, "metadata.json")
        data_path = os.path.join(path_to_res_folder, "data.txt")
        
        os.makedirs(path_to_res_folder, exist_ok=True)
        with open(metadata_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(metadata, indent=4, ensure_ascii=False))
        with open(data_path, "w", encoding="utf-8") as f:
            f.write(parse_result)
    