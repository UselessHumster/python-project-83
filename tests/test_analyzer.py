import pook
import pytest
import requests

from page_analyzer.analyzer import analyze_url, find_useful, is_reachable


@pook.on
def test_check_url():
    pook.get('https://test.test', reply=200, response_json={"You": "cool"})
    res = is_reachable('https://test.test')
    assert res

    pook.get('https://test.test', reply=404)
    res = is_reachable('https://test.test')
    assert not res


@pook.on
def test_analyze_url():
    pook.get('https://test.test', reply=200)
    res = analyze_url('https://test.test')
    assert res['status_code'] == 200

    pook.get('https://test.test', reply=404)
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
