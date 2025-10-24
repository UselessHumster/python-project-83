import pytest
import requests

from page_analyzer.analyzer import analyze_url, find_useful, is_reachable


def test_check_url(requests_mock):
    requests_mock.get('https://test.test', status_code=200, json={"You": "cool"})

    res = is_reachable('https://test.test')
    assert res

    requests_mock.get('https://test.test', status_code=404)
    res = is_reachable('https://test.test')
    assert not res


def test_analyze_url(requests_mock):
    requests_mock.get('https://test.test', status_code=200)
    res = analyze_url('https://test.test')
    assert res['status_code'] == 200

    requests_mock.get('https://test.test', status_code=404)
    res = analyze_url('https://test.test')
    assert res is None


@pytest.mark.vcr
def test_find_useful():
    expected = {'title': 'GitHub · Build and ship software on a single, '
                         'collaborative platform · GitHub',
                'description': "Join the world's most widely adopted, "
                               "AI-powered developer platform where millions "
                               "of developers, businesses, and the largest "
                               "open source community build software that "
                               "advances humanity.",
                'h1': 'Search code, repositories, users, '
                      'issues, pull requests...'}

    resp = requests.get('https://github.com')
    res = find_useful(resp.text)
    assert res == expected
