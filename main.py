# _*_ coding: utf-8 _*_
#scraping
import json
import time

from bs4 import BeautifulSoup
import requests


def get_data():

    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    pages_count = 10
    for i in range(1, pages_count + 1):
        url = f"https://timeshop.com.ua/ua/muzhskie-chasy-ua/page-{i}/"
        req = requests.get(url, headers)

        with open(f"data/page_{i}.html", "w", encoding="utf-8") as file:
            file.write(req.text)
        time.sleep(2)
        print(f"yes{i}")

    return pages_count + 1


def collect_data(pages_count):
    items_list = []
    for page in range(1, pages_count):
        with open(f"data/page_{page}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        col_title = soup.find_all("div", class_="ty-grid-list__item ty-quick-view-button__wrapper")
        for item in col_title:
            item_id = item.find("span", class_="ty-control-group__item").get_text()
            item_img_link = item.find("div", class_="ty-grid-list__image").find("img").get("src")
            item_link = item.find("div", class_="ty-grid-list__image").find("a").get("href")
            item_name = item.find("div", class_="ty-grid-list__item-name").find("a").get("title")
            item_price = item.find("div", class_="ty-grid-list__price").find("span", class_="ty-price-num").get_text()

            items_list.append(
                {
                    "ID": item_id,
                    "IMG": item_img_link,
                    "LINK": item_link,
                    "NAME": item_name,
                    "PRICE": item_price
                }
            )
    with open("data/data.json", "a") as file:
        json.dump(items_list, file, indent=4, ensure_ascii=False)


def main():
    pages_count = get_data()
    collect_data(pages_count=pages_count)


if __name__ == '__main__':
    main()


