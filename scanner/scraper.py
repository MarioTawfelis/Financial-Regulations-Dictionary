from bs4 import BeautifulSoup
import requests, urllib

"""
This Python script scrapes the latest Warnings issued by the FCA to be used in the News Feed
It parse through the document and adds a Scrape button after each Warning
"""


def get_latest():
    url = "https://www.fca.org.uk/news/search-results?np_category=warnings&start=1"

    page = requests.get(url)  # Load web page
    soup = BeautifulSoup(page.text, 'html.parser')  # Create soup to allow us to parse through the web page

    warnings = soup.findAll('li', attrs={
        "class": "search-item"})  # Scrape Warnings by parsing li tags with class attribute and value search-item

    for warning in warnings:
        warning['class'] = "list-group-item"  # Change value of attribute class to display Warnings using Bootstrap

        a_tag = warning.findAll('a', attrs={"class": "search-item__clickthrough"})
        source_url = a_tag[0].get('href')  # Get Warning URL

        scrape_btn = soup.new_tag('a', attrs={"class": "btn btn-primary",
                                              "href": "http://127.0.0.1:8000/documents/new?url=" + source_url})  # Create Scrappe button
        scrape_btn.string = "Scrape"

        last_div = warning('div')[-1]
        last_div.insert_after(scrape_btn)  # Add Scrape button after each Warning

    clean_html = str(warnings).replace("[", "").replace("]", "").replace(">,",
                                                                         ">")  # Sanitize HTML by removing uunwantd characters

    return clean_html
