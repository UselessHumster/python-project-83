import pook

from page_analyzer.analyzer import is_reachable, analyze_url

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