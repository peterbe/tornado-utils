def truncate_words(s, num, end_text='...'):
    """Truncates a string after a certain number of words. Takes an optional
    argument of what should be used to notify that the string has been
    truncated, defaults to ellipsis (...)"""
    length = int(num)
    words = s.split()
    if len(words) > length:
        words = words[:length]
        if not words[-1].endswith(end_text):
            words.append(end_text)
    return u' '.join(words)