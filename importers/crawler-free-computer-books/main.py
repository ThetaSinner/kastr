import requests
from bs4 import BeautifulSoup


def search_sitemap(base_url):
    r = requests.get("{}/sitemap.html".format(base_url))

    soup = BeautifulSoup(r.text, 'html.parser')

    links = soup.find_all("a")

    for link in links:
        href = link['href']
        if href is not None and len(href) > 1 and href.startswith('/'):
            if href == "/sitemap.html":
                continue

            read_sitemap_linked_page(base_url, "{}{}".format(base_url, href))
            break


def read_sitemap_linked_page(base_url, url):
    r = requests.get(url)

    print("Searching page")
    print(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    links = soup.find_all("a")

    for link in links:
        href = link['href']
        if href is not None and len(href) > 1 and href.startswith('/'):
            print("{}{}".format(base_url, href))


if __name__ == '__main__':
    base_url = 'http://freecomputerbooks.com'
    search_sitemap(base_url)
