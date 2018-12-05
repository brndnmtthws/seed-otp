import json
import os
import sys

import click
import seed_otp.crypto as scrypto
import seed_otp.generate as sgenerate
import seed_otp.words as swords
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


def pj(obj):
    """Print formatted JSON with beautiful colours."""
    click.echo(
        highlight(
            json.dumps(obj, indent=2, sort_keys=True),
            JsonLexer(),
            TerminalFormatter()
        )
    )


@cli.command()
@click.argument('num-words', type=int)
def generate(num_words):
    """Generate a secure OTP key for up to NUM_WORDS number of words.

    Make sure NUM_WORDS is at least as large as the number of seed words you
    use. It is normally 12 or 24 words. If you are unsure, use 24.
    """
    try:
        key = sgenerate.generate_key(num_words)
        pj({
            'success': True,
            'otp-key': key,
        })
    except Exception as e:
        pj({
            'success': False,
            'message': '{}: {}'.format(type(e).__name__, str(e)),
        })
        sys.exit(1)


@cli.command()
@click.argument('otp-key')
def check_key(otp_key):
    """Check OTP key for encoding or checksum errors."""
    try:
        (num_keys, keylist) = sgenerate.decode_key(otp_key)
        pj({
            'success': True,
            'num-keys': num_keys,
            'keylist': keylist,
        })
    except Exception as e:
        pj({
            'success': False,
            'message': '{}: {}'.format(type(e).__name__, str(e)),
        })
        sys.exit(1)


@cli.command()
@click.option('-l', '--language', default='english',
              help='Wordlist language from BIP-0039 wordlists. '
              'Must be one of: chinese_simplified, '
              'chinese_traditional, english, french, '
              'italian, japanese, korean, spanish.')
@click.option('-w', '--wordlist-file', type=click.Path(exists=True),
              help="Specify a custom wordlist. Don't change this unless you know what you're doing.")
@click.option('-o', '--include-options', is_flag=True,
              help='Include input options in output (may be useful for debugging).')
@click.option('-d', '--detail', is_flag=True, help='Include detail of word mapping.')
@click.argument('otp-key')
@click.argument('words', nargs=-1)
def encrypt(otp_key, language, wordlist_file, words, include_options, detail):
    """Encrypt seed words using an OTP key."""
    try:
        (num_keys, keylist) = sgenerate.decode_key(otp_key)
        (wordlist, word_to_idx) = swords.get_wordlist(
            language.lower(), wordlist_file)

        for word in words:
            if word not in word_to_idx:
                raise ValueError("'{}' is not in wordlist.".format(word))

        mapping = scrypto.encrypt(
            num_keys,
            keylist,
            wordlist,
            word_to_idx,
            words)

        obj = {
            'success': True,
            'encrypted-words': [m['ciphertext'] for m in mapping]
        }

        if include_options:
            obj.update({
                'otp-key': otp_key,
                'language': language,
                'wordlist-file': wordlist_file,
                'detail': detail,
            })
        if detail:
            obj.update({
                'mapping': mapping
            })

        pj(obj)
    except Exception as e:
        pj({
            'success': False,
            'message': '{}: {}'.format(type(e).__name__, str(e)),
        })
        sys.exit(1)


@cli.command()
@click.option('-l', '--language', default='english',
              help='Wordlist language from BIP-0039 wordlists. '
              'Must be one of: chinese_simplified, '
              'chinese_traditional, english, french, '
              'italian, japanese, korean, spanish.')
@click.option('-w', '--wordlist-file', type=click.Path(exists=True),
              help="Specify a custom wordlist. Don't change this unless you know what you're doing.")
@click.option('-o', '--include-options', is_flag=True,
              help='Include input options in output (may be useful for debugging).')
@click.option('-d', '--detail', is_flag=True, help='Include detail of word mapping.')
@click.argument('otp-key')
@click.argument('words', nargs=-1)
def decrypt(otp_key, language, wordlist_file, words, include_options, detail):
    """Decrypt seed words using an OTP key."""
    try:
        (num_keys, keylist) = sgenerate.decode_key(otp_key)
        (wordlist, word_to_idx) = swords.get_wordlist(
            language.lower(), wordlist_file)

        for word in words:
            if word not in word_to_idx:
                raise ValueError("'{}' is not in wordlist.".format(word))

        mapping = scrypto.decrypt(
            num_keys,
            keylist,
            wordlist,
            word_to_idx,
            words)

        obj = {
            'success': True,
            'decrypted-words': [m['message'] for m in mapping]
        }

        if include_options:
            obj.update({
                'otp-key': otp_key,
                'language': language,
                'wordlist-file': wordlist_file,
                'detail': detail,
            })
        if detail:
            obj.update({
                'mapping': mapping
            })

        pj(obj)
    except Exception as e:
        pj({
            'success': False,
            'message': '{}: {}'.format(type(e).__name__, str(e)),
        })
        sys.exit(1)


if __name__ == '__main__':
    cli()
