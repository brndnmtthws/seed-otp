import json

import click
import seed_otp.main as main
from click.testing import CliRunner


def test_check_key():
    runner = CliRunner()
    result = runner.invoke(
        main.check_key, ['AAwEyABkAHoA-wN4BH8GUAYSBlwEWQXGAzMya7y1']
    )
    assert result.exit_code == 0
    robj = json.loads(result.output)
    assert robj['success'] == True
    assert robj['keylist'] == [1224, 100, 122, 251,
                               888, 1151, 1616, 1554, 1628, 1113, 1478, 819]
    assert robj['num-keys'] == 12


def test_generate():
    runner = CliRunner()
    result = runner.invoke(
        main.generate, ['12']
    )
    assert result.exit_code == 0
    robj = json.loads(result.output)
    assert robj['success'] == True

    result = runner.invoke(
        main.check_key, [robj['otp-key']])
    assert result.exit_code == 0
    robj = json.loads(result.output)
    assert robj['success'] == True


def test_encrypt_and_decrypt():
    runner = CliRunner()
    result = runner.invoke(
        main.generate, ['12'])
    assert result.exit_code == 0
    robj = json.loads(result.output)
    assert robj['success'] == True

    otp_key = robj['otp-key']
    result = runner.invoke(
        main.check_key, [
            otp_key
        ]
    )
    assert result.exit_code == 0
    robj = json.loads(result.output)
    assert robj['success'] == True

    orig_seedlist = [
        "abandon",
        "ability",
        "able",
        "about",
        "above",
        "absent",
        "absorb",
        "abstract",
        "absurd",
        "abuse",
        "access",
        "accident",
    ]

    result = runner.invoke(
        main.encrypt, [
            '--include-options',
            '--detail',
            otp_key,
            *orig_seedlist,
        ]
    )
    assert result.exit_code == 0
    robj = json.loads(result.output)
    assert robj['success'] == True

    encrypted_seedlist = robj['encrypted-words']

    result = runner.invoke(
        main.decrypt, [
            '--include-options',
            '--detail',
            otp_key,
            *encrypted_seedlist,
        ]
    )

    assert result.exit_code == 0
    robj = json.loads(result.output)
    assert robj['success'] == True
    assert robj['decrypted-words'] == orig_seedlist


def test_check_fail():
    runner = CliRunner()
    result = runner.invoke(
        main.check_key, [
            'failkey'
        ]
    )
    assert result.exit_code == 1


def test_encrypt_fail():
    runner = CliRunner()
    result = runner.invoke(
        main.encrypt, [
            '--include-options',
            '--detail',
            'failkey',
            'word'
        ]
    )
    assert result.exit_code == 1
    robj = json.loads(result.output)
    assert robj['success'] == False

    result = runner.invoke(
        main.encrypt, [
            '--include-options',
            '--detail',
            'AAwEyABkAHoA-wN4BH8GUAYSBlwEWQXGAzMya7y1',
            'herpaderpword'
        ]
    )
    assert result.exit_code == 1
    robj = json.loads(result.output)
    assert robj['success'] == False


def test_decrypt_fail():
    runner = CliRunner()
    result = runner.invoke(
        main.decrypt, [
            '--include-options',
            '--detail',
            'failkey',
            'word'
        ]
    )
    assert result.exit_code == 1
    robj = json.loads(result.output)
    assert robj['success'] == False

    result = runner.invoke(
        main.decrypt, [
            '--include-options',
            '--detail',
            'AAwEyABkAHoA-wN4BH8GUAYSBlwEWQXGAzMya7y1',
            'herpaderpword'
        ]
    )
    assert result.exit_code == 1
    robj = json.loads(result.output)
    assert robj['success'] == False


def test_generate_fail():
    runner = CliRunner()
    result = runner.invoke(
        main.generate, [
            '10000000'
        ]
    )
    assert result.exit_code == 1
    robj = json.loads(result.output)
    assert robj['success'] == False
