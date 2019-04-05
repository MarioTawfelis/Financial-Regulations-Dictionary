from bs4 import BeautifulSoup
import requests, urllib


def get_latest():
    url = "https://www.fca.org.uk/news/search-results?np_category=warnings&start=1"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    warnings = soup.findAll('li', attrs={"class": "search-item"})

    for warning in warnings:
        warning['class'] = "list-group-item"

        a_tag = warning.findAll('a', attrs={"class": "search-item__clickthrough"})
        source_url = a_tag[0].get('href')

        scrape_btn = soup.new_tag('a', attrs={"class": "btn btn-primary",
                                              "href": "http://127.0.0.1:8000/documents/new?url=" + source_url})
        scrape_btn.string = "Scrape"

        last_div = warning('div')[-1]
        last_div.insert_after(scrape_btn)

    clean_html = str(warnings).replace("[", "").replace("]", "").replace(">,", ">")

    return clean_html
