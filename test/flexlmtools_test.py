from flexlmtools import parse_query, is_valid_server_name
import pytest

APP_FEATURES = {'feat1': (2, 0), 'feat2': (5, 1),
                'feat6': (3, 3), 'feat-add': (2, 0),
                'feat_opt': (1, 1)}


def test_parse_query():
    with open('./test/app-features.txt', 'r') as f:
        lines = f.read()

    def check(feature):
        dct = parse_query(lines, features=[feature])
        assert feature in dct
        assert dct[feature] == APP_FEATURES[feature]

    check('feat1')
    check('feat2')
    check('feat6')
    check('feat-add')
    check('feat_opt')

    dct = parse_query(lines, features=['feat3'])
    # Check if dct is empty
    assert not dct

    dct = parse_query(lines)
    assert all(feature in dct for feature in APP_FEATURES)
    assert all(dct[feature] == values for feature,
               values in APP_FEATURES.items())

def test_is_valid_server_name():
    assert is_valid_server_name('6200@test-server.org')
    assert not is_valid_server_name('0123@test-serv')
    assert not is_valid_server_name('1234@test_serv')
    assert not is_valid_server_name('3100@test#serv')