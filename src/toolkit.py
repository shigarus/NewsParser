# -*- coding: utf-8 -*-


def get_site_name(url):
    """
    :param url: basestring
    """
    if not isinstance(url, basestring):
        raise TypeError('url has to be basestring instance')
    url = morph_url(url)
    return url.split('/')[0]


def morph_url(url):
    """
    Morph url like
        http://default.ru/news/2013/03/dtp/ => default.ru/news/2013/03/dtp
    :param url: basestring
    :return: basestring
    """
    if not isinstance(url, basestring):
        raise TypeError('url has to be basestring instance')

    if url.startswith('http://'):
        url = url[7:]
    if url.startswith('www.'):
        url = url[4:]
    if url.endswith('/'):
        url = url[:-1]

    return url