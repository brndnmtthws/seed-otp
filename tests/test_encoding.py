import secrets

import pytest
from seed_otp import generate


def test_generate_key(mocker):
    mock = mocker.patch('secrets.randbelow')
    for num_keys in [12, 24]:
        key = generate.generate_key(num_keys)
        assert key in [
            'AAwAAQABAAEAAQABAAEAAQABAAEAAQABAAF16fyM',
            'ABgAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAGNCTq4',
        ]
        mock.assert_has_calls([mocker.call(2048)] * num_keys)

        (nkeys, keys) = generate.decode_key(key)
        assert nkeys == num_keys
        assert keys == [1] * num_keys


def test_encode_key():
    key = generate.encode_key(1, [1])
    assert key == 'AAEAAXbMWAU'

    key = generate.encode_key(2, [1, 2])
    assert key == 'AAIAAQAC2GT05A'

    key = generate.encode_key(12, [42] * 12)
    assert key == 'AAwAKgAqACoAKgAqACoAKgAqACoAKgAqACpsK2wb'

    key = generate.encode_key(24, [42] * 24)
    assert key == 'ABgAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoDlSQ4'

    key = generate.encode_key(48, [42] * 48)
    assert key == 'ADAAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACpHAFeS'


def test_decode_key():
    (num_keys, keylist) = generate.decode_key('AAEAAXbMWAU')
    assert num_keys == 1
    assert keylist == [1]

    (num_keys, keylist) = generate.decode_key('AAIAAQAC2GT05A')
    assert num_keys == 2
    assert keylist == [1, 2]

    (num_keys, keylist) = generate.decode_key(
        'AAwAKgAqACoAKgAqACoAKgAqACoAKgAqACpsK2wb')
    assert num_keys == 12
    assert keylist == [42] * 12

    (num_keys, keylist) = generate.decode_key(
        'ABgAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoDlSQ4')
    assert num_keys == 24
    assert keylist == [42] * 24

    (num_keys, keylist) = generate.decode_key(
        'ADAAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACoAKgAqACpHAFeS')
    assert num_keys == 48
    assert keylist == [42] * 48


def test_decode_invalid_key():
    with pytest.raises(generate.DecodingError):
        generate.decode_key('ABEAAXbMWAU')

    with pytest.raises(generate.DecodingError):
        generate.decode_key('AAz-JR5N')
