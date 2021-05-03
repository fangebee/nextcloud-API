# -*- coding: utf-8 -*-
"""
Tools for python2/3 unicode compatibility
"""
import six


def encode_requests_password(word):
    """
    Convert the string to bytes (readable by the server)

    :param word: input string
    :returns:    bytes with appropriate encoding
    """
    if isinstance(word, bytes):
        return word
    else:
        ret = word
        if six.PY2:
            if isinstance(word, unicode):
                # trick to work with tricks in requests lib
                ret = word.encode('utf-8').decode('latin-1')
        else:
            try:
                ret = bytes(word, 'ascii')
            except UnicodeEncodeError:
                ret = bytes(word, 'utf-8')
        return ret


def encode_string(string):
    """Encodes a unicode instance to utf-8. If a str is passed it will
    simply be returned

    :param string: str or unicode to encode
    :returns     : encoded output as str
    """
    if six.PY2:
        if isinstance(string, unicode):
            return string.encode('utf-8')
    return string

# from six.moves.urllib import parse
# def prepare_url(s):
#     if six.PY2 and isinstance(s, unicode):  # noqa: F821
#         return parse.urlparse(s).path
#     return s