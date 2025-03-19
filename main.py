import json
import os
from typing import List
import requests
from bs4 import BeautifulSoup

from ticket import Ticket


RES_FOLDER = "results"


def main():
    for id in range(1, 1600):
        url_to_parse = f"https://mfc66.ru/services/item?id={id}"
        parsed_tickets = parse_mfc_tickets_from_url(url_to_parse, id)
        if len(parsed_tickets) == 0:
            print(f"Skipping {id}")
            continue
        for ticket in parsed_tickets:
            save_ticket(ticket)
        
        


def parse_mfc_tickets_from_url(url: str, url_id: int) -> List[Ticket]:
    response = fetch_url(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if check_if_page_is_empty(soup):
        print(" EMPTY PAGE detected")
        return []
    if check_if_url_contains_li(soup):
        return [] # NOT SUPPORTED YET
    else:
        captions_text = get_div_text_content(soup, "page-caption")
        content_text = get_div_text_content(soup, "content-block")
        ticket_content = captions_text + content_text
        ticket_meta = {
            "topic": captions_text, "link": url, "id": str(url_id)
        }
        return [Ticket(ticket_content, ticket_meta)]



def fetch_url(url: str) -> requests.Response:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response
    
    
def check_if_url_contains_li(soup: BeautifulSoup) -> bool:
    return len(soup.find_all('div', class_="accordion")) > 0


def check_if_page_is_empty(soup: BeautifulSoup) -> bool:
    return len(soup.find('div', class_="page-caption").get_text(strip=True)) == 0
 

def save_ticket(ticket: Ticket):
    path_to_res_folder = os.path.join(RES_FOLDER, f"{ticket.metadata["id"]}")
    metadata_path = os.path.join(path_to_res_folder, "metadata.json")
    data_path = os.path.join(path_to_res_folder, "data.txt")
    os.makedirs(path_to_res_folder, exist_ok=True)
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(ticket.metadata, indent=4, ensure_ascii=False))
    with open(data_path, "w", encoding="utf-8") as f:
        f.write(ticket.content)
  
    
def get_div_text_content(soup: BeautifulSoup, classname: str) -> str:
    class_encounters = soup.find_all('div', class_=classname)
    res_text = ""
    for content in class_encounters:
        res_text += content.get_text(strip=True)
        res_text += "\n\n"
    return res_text.replace(":", ": ")


if __name__ == '__main__':
    main()
    