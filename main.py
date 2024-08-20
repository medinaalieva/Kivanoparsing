import requests
from bs4 import BeautifulSoup as BS
import csv 

URL = "https://www.kivano.kg/mobilnye-telefony"

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BS(html, "lxml")
    catalog = soup.find("div", class_="product-index")
    smarts = catalog.find_all("div", "item product_listbox oh")
    for smart in smarts:
        try:
            title = smart.find("div", class_="listbox_img pull-left").find("img").get("alt")
        except AttributeError:
            title = ""
        try:
            image = smart.find("img").get("src")
            image = f"https://www.kivano.kg{image}"
        except AttributeError:
            image = ""
        try:
            price = smart.find("div", class_="listbox_price text-center").find("strong").text
        except AttributeError:
            price = ""

        data = {
            "title": title,
            "image": image,
            "price": price,
        }

        write_csv(data)

def write_csv(data):
    with open("kivano_kg_mobilnye-telefony.csv", "a",) as csv_file:
        name = ["title", "price", "image"]
        writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=name)
        writer.writerow(data)


def main():
    URL = "https://www.kivano.kg/mobilnye-telefony"
    html = get_html(URL)
    for page in range(1, 18):
        url = f"https://www.kivano.kg/mobilnye-telefony?page={page}-{page-1}"
        html = get_html(url)
        get_data(html)

main()
