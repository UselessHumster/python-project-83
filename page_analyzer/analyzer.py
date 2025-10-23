import requests


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

    return {'status_code': resp.status_code}
