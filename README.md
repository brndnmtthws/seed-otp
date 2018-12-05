[![Build Status](https://travis-ci.org/brndnmtthws/seed-otp.svg?branch=master)](https://travis-ci.org/brndnmtthws/seed-otp) [![Maintainability](https://api.codeclimate.com/v1/badges/679cd32dba7a27f9bb4d/maintainability)](https://codeclimate.com/github/brndnmtthws/seed-otp/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/679cd32dba7a27f9bb4d/test_coverage)](https://codeclimate.com/github/brndnmtthws/seed-otp/test_coverage) [![PyPI version](https://badge.fury.io/py/seed-otp.svg)](https://badge.fury.io/py/seed-otp)

# seed-otp

`seed-otp` is a Python-based one-time pad CLI tool for storing your Bitcoin seed
mnemonic words securely using multi-factor auth.

## Background

### The Problem

You have an HD wallet such as a Trezor or Ledger for storing your Bitcoin,
and you would like to store your seed mnemonic phrase. You may also
want to store multiple copies of your seed in different places.
Unfortunately, if any one of those copies of your seed becomes compromised,
anyone with access to the seed can now take all your coins, and buy
themselves
a lambo.

Normally you would not need access to your seed mnemonic. However, should
something happen to your wallet (perhaps you lose it, or it breaks), you may
need to restore the wallet using the seed phrase.

### This Solution

Use a [one-time pad](https://en.wikipedia.org/wiki/One-time_pad) with
[multi-factor
authentication](https://en.wikipedia.org/wiki/Multi-factor_authentication).

By combining mult-factor auth (something you know plus something you have)
and one-time pad encryption, you have a simple yet extremely hard to crack
solution. Your OTP key and seed mnemonic are stored separately, making it
onerous to obtain both. If someone _does_ obtain either your mnemonic or OTP
key, you would have time to move your funds to a new wallet with a brand new seed and OTP key.

Your auth factors are:

- **Something you know**: A one-time pad key which you have stored securely in
  a password manager, which is locked with a password only you know. The
  password DB is backed up securely.
- **Something you have**: An encrypted mnemonic seed phrase stored on archival
  paper or another long term physical cold storage device. The phrase itself
  looks like a normal mnenomic phrase, which provides plausible deniability,
  and does not indicate to anyone who might find the phrase _how_ it's
  actually used.

### Caveats, Limitations, Gotchas

- To use this tool, you need to enter the seed words into a computer. If your
  computer is compromised, someone could still use a keylogger or other tool to
  capture the seed mnemonic. Only use this tool if you trust the computer you
  are using.

### Other Solutions

There are a variety of other solutions to this problem, some of which may be
more appropriate for your needs. Let's go over some of the alternatives and
discuss why they might not be appropriate:

1. Custody with a third party, such as Coinbase.
   - The main problem with any third party custody service is that you must
     place complete trust in that third party.
   - Custody providers are not immune to crime, theft, rogue employees,
     mistakes, going out of business, or government intervention. _Rekt_.
2. The Horcrux design (using a multi-signature scheme).
   - This pattern is based on the idea of storing small pieces of your seed
     phrase in several different places, much like Voldemort did with his soul
     in Harry Potter.
   - While it's not impossible to do this on your own, it's logistically
     tricky and prone to error.
   - There is at least one company which provides this option as a service,
     but at the time of writing they're asking for several thousand dollars
     per year in subscription fees, an amount that is both absurd and out of
     reach for normal people. _Rekt_ because you have no money left.
3. Storing your seed phrase in a super secret place and hoping nobody finds
   it.
   - This is equivalent to burying a chest full of treasure in your backyard
     and hoping nobody looks there. _Rekt_ when your neighbour buys a metal
     detector.
4. Store the seed phares itself using a password manager.
   - The main downside is that you do not have multi-factor auth: if someone
     gains access to your password manager, you will be _rekt_.

## Quickstart

### Checklist

Before using this tool, you should have a few things:

- [x] Get a decent hardware wallet from a reputable vendor. 2 popular options
      are [Trezor](https://trezor.io/) and [Ledger](https://www.ledger.com/).
- [x] Get a password manager, and learn to use it (if you haven't already). A
      few good options are [KeepPassX](https://www.keepassx.org/),
      [1Password](https://1password.com/), or [BitWarden](https://bitwarden.com/).
      Make sure your passwords are backed up, and test the restore process.
- [x] Figure out a good way to store your mnemonic seed phrase, such as using
      archival paper or a metal seed storage product (check out [@lopp's stress
      test
      here](https://medium.com/@lopp/metal-bitcoin-seed-storage-stress-test-21f47cf8e6f5)).
- [x] Have a safe place to store the seed mnemonic, such as in an actual safe,
      or a safe deposit box.
- [x] Make sure you have a secure computer to run the software. It should be
      running an up-to-date and secure OS. Avoid using any computers which might be
      controlled by third parties (such as a work computer, or your friend's
      computer). If you want to be extra safe, consider using a [privacy OS such as
      Tails](https://tails.boum.org/)

### Install from PyPI

```ShellSession
$ pip install seed-otp
```

### Generate an OTP key

```ShellSession
$ seed-otp generate 12
{
  "otp-key": "AAwCnwGIAe0EWABWAI4AkAMjAFQBLgZjB1T1PJtz",
  "success": true
}
```

Store the key above in your password management tool.

### Encode your seed mnemonic using the OTP

```ShellSession
$ seed-otp encrypt AAwCnwGIAe0EWABWAI4AkAMjAFQBLgZjB1T1PJtz abandon ability able about above absent absorb abstract absurd abuse access accident
{
  "encrypted-words": [
    "fault",
    "couple",
    "digital",
    "merge",
    "area",
    "bar",
    "barrel",
    "grab",
    "argue",
    "cheap",
    "soap",
    "typical"
  ]
}
```

Store the phrase above in your safe place.

### Decode your seed mnemonic using the OTP

```ShellSession
$ seed-otp decrypt AAwCnwGIAe0EWABWAI4AkAMjAFQBLgZjB1T1PJtz fault couple digital merge area bar barrel grab argue cheap soap typical
{
  "decrypted-words": [
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
    "accident"
  ]
}
```

## Synopsis

    Usage: seed-otp [OPTIONS] COMMAND [ARGS]...

    Options:
      -h, --help  Show this message and exit.

    Commands:
      check-key  Check OTP key for encoding or checksum errors.
      decrypt    Decrypt seed words using an OTP key.
      encrypt    Encrypt seed words using an OTP key.
      generate   Generate a secure OTP key for up to NUM_WORDS number of words.

## Implementation Details

### OTP Key

The OTP key is a URL-safe base64 encoded key (without padding) composed of N
subkeys, where N is the number of keys specified at creation time. The values
are stored as big-endian short unsigned integers (2-bytes each). The last 4
bytes of the OTP key is the first 4 bytes of the SHA256 digest of the
preceeding bytes.

    0                   1
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |         Number of Keys        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    \                               /
    /   Keylist (variable length)   \
    \                               /
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                               |
    +            Checksum           +
    |                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

BIP-0039 uses 11 bits per word, but in this scheme we're using 16 bits per
word. This is mainly for simplicity, with the trade-off of using more bytes.
It also allows the possibilty of using larger wordlists (of up to 65536
words).

### Encrypting/decrypting words

Below is some pseudocode for encrypting/decrypting. Assume that the words and
keys are mapped to integers representing an index position in the wordlist.

To encrypt a word, the algorithm is as follows:

    ciphertext = (word + key) mod 2048

To decrypt a word, do the following:

    word = (ciphertext - key) mod 2048

You could perform the encryption/decryption using pen and paper if you feel
the need to do so. This would prevent the necessity of typing your seed words
into a computer. Naturally, you could also generate your own keys and store
those offline as well. For practical purposes, however, this is probably
unnecessary.

## Tip jar

- BTC: 3EEAE1oKEMnmHGU5Qxibv9mBQyNnes8j8N
