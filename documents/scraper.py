from bs4 import BeautifulSoup
import requests, urllib

html_header = "<!DOCTYPE HTML><html><head><meta charset='UTF-8'></head>"
content = ""


def find_regulator(url):
    if "https://www.fca.org.uk/news/warnings/" in url:
        scrapeFCA(url)
    elif "https://www.ecb.europa.eu/press/" in url:
        scrapeECB(url)

    return content


def scrapeFCA(url):
    global content
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    soup.find('div', attrs={"class": "page-feedback"}).decompose()
    soup.find('div', attrs={"class": "header__social-links"}).decompose()
    soup.find('div', attrs={"class": "rhn"}).decompose()

    content_box = soup.findAll('div', attrs={"class": "container"})[8]

    content = html_header + str(content_box)


def scrapeECB(url):
    global content
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html5lib')

    soup.find('div', attrs={"class": "footer footer-address"}).decompose()
    soup.find('div', attrs={"class": "hiddenCrossnav"}).decompose()
    soup.find('a', attrs={"class": "arrow"}).decompose()

    images = soup.findAll('img')
    if images:
        for image in images:
            image['src'] = "https://www.ecb.europa.eu/press/pr/date/2019/html/" + image['src']

    content_box = soup.find('div', attrs={"class": "ecb-pressContent"})

    content = html_header + str(content_box)

