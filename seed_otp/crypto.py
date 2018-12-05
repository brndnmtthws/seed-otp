

def encrypt(
        num_keys,
        keylist,
        wordlist,
        word_to_idx,
        words):
    """Encrypt words using OTP word indexes."""
    if len(words) > num_keys:
        raise ValueError("Number of input words exceeds key length")
    result = []
    for i in range(0, len(words)):
        m = words[i]
        m_i = word_to_idx[m]
        k = keylist[i]
        c_i = (m_i + k) % len(wordlist)
        result.append({
            'message': wordlist[m_i],
            'ciphertext': wordlist[c_i]
        })
    return result


def decrypt(
        num_keys,
        keylist,
        wordlist,
        word_to_idx,
        words):
    """Encrypt words using OTP word indexes."""
    if len(words) > num_keys:
        raise ValueError("Number of input words exceeds key length")
    result = []
    for i in range(0, len(words)):
        c = words[i]
        c_i = word_to_idx[c]
        k = keylist[i]
        m_i = (c_i - k) % len(wordlist)
        result.append({
            'message': wordlist[m_i],
            'ciphertext': wordlist[c_i]
        })
    return result
