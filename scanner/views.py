from django.shortcuts import render
from .scraper import get_latest


def home(request):
    news_feed = get_latest()

    return render(request, 'scanner/home.html', {'news_feed': news_feed})


def scrape(request, url):
    pass
