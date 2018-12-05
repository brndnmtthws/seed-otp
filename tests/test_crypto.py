import random

import pytest
from seed_otp import crypto, generate


def test_encrypt():
    result = crypto.encrypt(
        3,
        [1, 2, 3],
        ["a", "b", "c", "d"],
        {"a": 0, "b": 1, "c": 2, "d": 3},
        ["a", "b", "c"]
    )
    assert [r['ciphertext'] for r in result] == ['b', 'd', 'b']


def test_encrypt_invalid_keynum():
    with pytest.raises(ValueError):
        result = crypto.encrypt(
            1,
            [1, 2, 3],
            ["a", "b", "c", "d"],
            {"a": 0, "b": 1, "c": 2, "d": 3},
            ["a", "b", "c"]
        )


def test_decrypt():
    result = crypto.decrypt(
        3,
        [1, 2, 3],
        ["a", "b", "c", "d"],
        {"a": 0, "b": 1, "c": 2, "d": 3},
        ['b', 'd', 'b']
    )
    assert [r['message'] for r in result] == ['a', 'b', 'c']


def test_decrypt_invalid_keynum():
    with pytest.raises(ValueError):
        result = crypto.decrypt(
            1,
            [1, 2, 3],
            ["a", "b", "c", "d"],
            {"a": 0, "b": 1, "c": 2, "d": 3},
            ["a", "b", "c"]
        )


@pytest.fixture
def wordlist():
    from seed_otp import words
    return words.get_wordlist('english', None)


@pytest.fixture(params=[1, 2, 3, 12, 24, 48])
def num_keys(request):
    return request.param


@pytest.fixture(params=list(range(0, 10)))
def iteration(request):
    return request.param


def test_encrypt_and_decrypt(wordlist, num_keys, iteration):
    # choose random words
    words = []
    while len(words) < num_keys:
        w = random.choice(wordlist[0])
        if w not in words:
            words.append(w)

    key = generate.generate_key(num_keys)
    (num_keys, word_indexes) = generate.decode_key(key)

    encrypted = crypto.encrypt(
        num_keys,
        word_indexes,
        wordlist[0],
        wordlist[1],
        words
    )

    decrypted = crypto.decrypt(
        num_keys,
        word_indexes,
        wordlist[0],
        wordlist[1],
        [r['ciphertext'] for r in encrypted]
    )

    assert [r['message'] for r in decrypted] == words
