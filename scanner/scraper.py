from bs4 import BeautifulSoup
import requests, urllib


def get_latest():
    url = "https://www.fca.org.uk/news/search-results?np_category=warnings&start=1"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    warnings = soup.findAll('li', attrs={"class": "search-item"})

    for warning in warnings:
        warning['class'] = "list-group-item"

    clean_html = str(warnings).replace("[", "").replace("]", "").replace(">,", ">")

    return clean_html
