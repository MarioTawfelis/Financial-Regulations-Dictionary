from bs4 import BeautifulSoup
import requests, urllib

html_header = "<!DOCTYPE HTML><html><head><meta charset='UTF-8'></head>"


def scrapeFCA(url):
    if "https://www.fca.org.uk/news/warnings/" in url:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        soup.find('div', attrs={"class": "page-feedback"}).decompose()
        soup.find('div', attrs={"class": "header__social-links"}).decompose()
        soup.find('div', attrs={"class": "rhn"}).decompose()

        content_box = soup.findAll('div', attrs={"class": "container"})[8]

    return html_header + str(content_box)
