from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def normalize_url(url):
    parsed = urlparse(url)
    return f'{parsed.scheme}://{parsed.netloc}'


def is_reachable(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.ConnectionError:
        return False
    except requests.HTTPError:
        return False
    return resp


def analyze_url(url: str):
    if not (resp := is_reachable(url)):
        return None

    data = {'status_code': resp.status_code}
    useful_info = find_useful(resp.text)
    return data | useful_info


def find_useful(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    h1 = soup.find('h1').get_text().strip() if soup.find('h1') else ''
    return {'title': title, 'description': description, 'h1': h1}
