from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from data import DataAccess
from data import DataModel

base_url = 'http://freecomputerbooks.com'
searched_pages = set()

run_in_test_mode = False


def is_http(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme == 'http' or parsed.scheme == 'https'
    except UnicodeEncodeError:
        print("Bad URL {}".format(url))
        return False


def search_sitemap():
    start_url = "{}/sitemap.html".format(base_url)
    searched_pages.add(start_url)

    r = requests.get(start_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    links = soup.find_all("a")

    for link in links:
        href = link['href']
        if href is not None and len(href) > 1 and href.startswith('/'):
            if href in searched_pages:
                continue

            seed_url = "{}{}".format(base_url, href)
            print("Starting new seed page {}".format(seed_url))
            read_sitemap_linked_page(seed_url, list(seed_url))


def read_sitemap_linked_page(url, url_trace):
    if not is_http(url):
        print('(read_sitemap_linked_page) Invalid URL scheme [{}]'.format(url))
        return

    r = requests.get(url)

    if url in searched_pages:
        return

    searched_pages.add(url)

    print("Searching page")
    print(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    book_titles = soup.find_all(id="booktitle")
    if book_titles:
        print("Suspected book on page [{}]".format(url))
        find_links_to_download_pages(soup, url_trace)
        return

    links = soup.find_all("a")

    for link in links:
        if 'href' not in link:
            continue

        href = link['href']
        if href is not None and len(href) > 1 and href.startswith('/'):
            next_url = "{}{}".format(base_url, href)

            new_trace = url_trace.copy()
            new_trace.append(next_url)
            read_sitemap_linked_page(next_url, new_trace)


def find_links_to_download_pages(url, url_trace):
    if not is_http(url):
        print('(download_from_page) Invalid URL scheme [{}]'.format(url))
        return

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    book_titles = soup.find_all(id="booktitle")

    meta = list()
    list_items = book_titles[0].ul.find_all("li")
    for li in list_items:
        key = li.contents[0].contents[0]
        value = li.contents[1].strip()
        if not key or not value:
            continue

        meta.append((key, value))

    print("Extracted meta {}".format(meta))

    bolds = soup.find_all('b')
    for b in bolds:
        if 'Download' in b.contents[0]:
            print("Found download links section")

            next_sibling = b.next_sibling
            while next_sibling is not None and next_sibling.name != 'ul':
                next_sibling = next_sibling.next_sibling

            if next_sibling is None:
                print("Didn't find a list which might contain links")
                continue

            download_links = next_sibling.find_all('a')
            if not download_links:
                print("No download links found in expected section")
                continue

            for download_link in download_links:
                download_page_url = download_link["href"]
                new_trace = url_trace.copy()
                new_trace.append(download_page_url)
                download_from_page(download_page_url, new_trace, meta)


def download_from_page(url, url_trace, meta):
    if not is_http(url):
        print('(download_from_page) Invalid URL scheme [{}]'.format(url))
        return

    download_links = identify_download_links(url)

    if len(download_links) == 0:
        print('No download links found on {}'.format(url))
        return

    if len(download_links) > 1:
        print('Multiple links found')

    download_url = next(iter(download_links))
    if run_in_test_mode:
        print("Identified download URL {}, stopping in test mode".format(download_url))
        return

    data_model = DataModel()
    data_model.download_page_url = url
    data_model.download_url = download_url

    new_trace = url_trace.copy()
    new_trace.append(download_url)
    data_model.url_trace_csv = ','.join(new_trace)

    data_model.meta_csv = ','.join(["{},{}".format(x[0], x[1]) for x in meta])

    if not is_http(download_url):
        print('(download_from_page) Invalid download URL scheme [{}]'.format(download_url))
        return

    file = requests.get(download_url)
    open("{}.pdf".format(data_model.id), 'wb').write(file.content)

    access = DataAccess()
    access.store(data_model)

    exit(1)


def identify_download_links(url):
    r = requests.get(url, allow_redirects=True)

    soup = BeautifulSoup(r.text, 'html.parser')
    download_links = set()
    links = soup.find_all('a')
    for link in links:
        print(link["href"])
        if "href" not in link:
            continue

        href = link["href"]
        print(href)

        if 'pdf' in href:
            download_links.add(href)

    return download_links


if __name__ == '__main__':
    search_sitemap()

    #run_in_test_mode = True
    # find_links_to_download_pages("http://freecomputerbooks.com/Essentials-of-Geographic-Information-Systems.html", list())
    # result = identify_download_links("https://archive.org/details/2011EssentialsOfGeographicInformationSystems/")
    # print(result)
