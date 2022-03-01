def is_broken_bin(s):
    pat = '12'
    i = False
    for char in s:
        if char != pat[i]:
            return True
        i = not i
    return False


def is_broken_any_len(s, pat):
    length = len(pat)
    for i in range(len(s)):
        if s[i] != pat[i % length]:
            return True
    return False
