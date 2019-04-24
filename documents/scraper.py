from bs4 import BeautifulSoup
import requests, urllib

html_header = "<!DOCTYPE HTML><html><head><meta charset='UTF-8'></head>"
content = ""


# Check if website is supported and call relevant scraping function
def find_regulator(url):
    if "https://www.fca.org.uk/news/warnings/" in url:
        scrapeFCA(url)
    elif "https://www.ecb.europa.eu/press/" in url:
        scrapeECB(url)
    elif "https://www.esma.europa.eu/press-news/esma-news/" in url:
        scrapeESMA(url)
    elif "https://www.sec.gov/news/press-release/" in url:
        scrapeSEC(url)
    else:
        return None

    return content


def scrapeFCA(url):
    global content
    page = requests.get(url)  # Load web page
    soup = BeautifulSoup(page.text, 'html.parser')  # Create soup to allow us to parse through the web page

    # Clean web page but removing unwanted content such as social media links and feedback forms
    soup.find('div', attrs={"class": "page-feedback"}).decompose()
    soup.find('div', attrs={"class": "header__social-links"}).decompose()
    soup.find('div', attrs={"class": "rhn"}).decompose()

    content_box = soup.findAll('div', attrs={"class": "container"})[8]  # Scrape content (i.e. regulatory update)

    content = html_header + str(content_box)


def scrapeECB(url):
    global content
    page = requests.get(url)  # Load web page
    soup = BeautifulSoup(page.text, 'html5lib')  # Create soup to allow us to parse through the web page

    # Clean web page but removing unwanted content such as social media links and feedback forms
    soup.find('div', attrs={"class": "footer footer-address"}).decompose()
    soup.find('div', attrs={"class": "hiddenCrossnav"}).decompose()
    soup.find('a', attrs={"class": "arrow"}).decompose()

    # Change relative paths to absolute to show media content as displayed on original web page
    images = soup.findAll('img')
    if images:
        for image in images:
            image['src'] = "https://www.ecb.europa.eu/press/pr/date/2019/html/" + image['src']

    content_box = soup.find('div', attrs={"class": "ecb-pressContent"})  # Scrape content (i.e. regulatory update)

    content = html_header + str(content_box)


def scrapeESMA(url):
    global content
    page = requests.get(url)  # Load web page
    soup = BeautifulSoup(page.text, "html5lib")  # Create soup to allow us to parse through the web page

    # Clean web page but removing unwanted content such as social media links and feedback forms
    soup.find('div', attrs={"class": "esmapage_menu-fixed"}).decompose()

    content_box = soup.find('div', attrs={"id": "esmapage_main-content"})  # Scrape content (i.e. regulatory update)

    content = html_header + str(content_box)


def scrapeSEC(url):
    global content
    page = requests.get(url)  # Load web page
    soup = BeautifulSoup(page.text, "html5lib")  # Create soup to allow us to parse through the web page

    content_box = soup.find('div',
                            attrs={"class": "content aside press-release"})  # Scrape content (i.e. regulatory update)

    content = html_header + str(content_box)
