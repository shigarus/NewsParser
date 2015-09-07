# -*- coding: utf-8 -*-
import re

import grab
import lxml.html


H_TAGS = ['h{}'.format(i) for i in range(1, 7)]
TAGS_TO_SEPARATE = H_TAGS + ['p', 'li', ]
TAGS_PARAGRAPHS = H_TAGS + ['p', ]

MANY_LINE_ENDINGS = re.compile('(\n|\r\n){3,}')
TRASH_SPACES = re.compile(' {2,}')
TRASH_SYMBOLS = re.compile('[\r\n\t]')


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


class HtmlTextExtractor(object):

    def __init__(self, rules):
        self._rules = rules
        self._grabber = grab.Grab()
        self._url = None
        self._always_exlude = ['script', 'noscript']

    @property
    def _include_selectors(self):
        """
        :return: list of css selectors
        """
        site_name = get_site_name(self._url)
        return self._rules[site_name]['include']

    @property
    def _exclude_selectors(self):
        """
        :return: list of css selectors
        """
        site_name = get_site_name(self._url)
        site_exclude = self._rules[site_name]['exclude']
        return site_exclude + self._always_exlude

    def _go_url(self):
        # grabber can lead wrong page if url
        # won't start with http://
        if not self._url.startswith('http://'):
            url = u''.join((
                u'http://',
                self._url
            ))
        else:
            url = self._url

        self._grabber.go(url)

    @property
    def _tree(self):
        return self._grabber.doc.tree

    def get_text(self, url):
        if not isinstance(url, basestring):
            raise TypeError('url has to be basestring instance')

        self._url = url
        self._go_url()

        for selector in self._exclude_selectors:
            for node in self._tree.cssselect(selector):
                node.getparent().remove(node)

        texts = []
        for selector in self._include_selectors:
            for node in self._tree.cssselect(selector):
                text = html_to_readable(node)
                texts.append(text)
        return u'\r\n'.join(texts)


def del_trash_symbols(line):
    if not isinstance(line, basestring):
        raise TypeError('line has to be basestring instance')
    line = re.sub(TRASH_SYMBOLS, ' ', line)
    line = re.sub(TRASH_SPACES, ' ', line)
    return line.strip()


def html_to_readable(element):
    """
    Rules:
        length - 80 symbols
        word wrap
        paragraphs and title separated by new line
        <a href='url'>sometext</a> transforms to sometext[url]

    :param element: lxml.html.HtmlElement
    :return: unicode
    """
    if not isinstance(element, lxml.html.HtmlElement):
        raise TypeError('element has to be lxml.html.HtmlElement instance')

    # process inner of <a> tags to avoid collisions
    # with adding url after <a> tag
    for node in element.cssselect('a'):
        href = node.get('href')
        if not href:
            continue
        inner_tags_to_text(node)
        href = u'[{}]'.format(href)
        tail = node.tail or u''
        node.tail = u''.join((
            href,
            tail
        ))

    # process inner of h* tags to avoid
    # broken titles separating
    for tag in TAGS_PARAGRAPHS:
        for node in element.cssselect(tag):
            inner_tags_to_text(node)

    inner_tags_to_text(element)
    text = element.text
    # remove starts and ends trash symbols
    while text[0] in ('\r', '\n'):
        text = text[1:]
    while text[-1] in ('\r', '\n'):
        text = text[:-1]

    return text


def inner_tags_to_text(element):
    """
    Replace inner tags to text
    :param element: lxml.html.HtmlElement
    """
    if not isinstance(element, lxml.html.HtmlElement):
        raise TypeError('element has to be lxml.html.HtmlElement instance')
    paragraphs = []
    cur_str = u''
    for node in element.iter():
        # need tail only for inner tag
        if node is element:
            tail = u''
        else:
            tail = node.tail or u''

        tag = node.tag

        # check if tag closes current paragraph
        if tag == 'br':
            paragraphs.append(cur_str)
            cur_str = u''

        if tag in TAGS_TO_SEPARATE:
            paragraphs.append(cur_str)
            if tag != 'li':
                paragraphs.append(u'')
            text = node.text
            if text:
                paragraphs.append(node.text)
            cur_str = u''
        else:
            cur_str = ''.join((
                cur_str,
                node.text or u'',
                tail
            ))

    paragraphs.append(cur_str)

    # need to delete inner tags to not include their text again
    # if we will use this fnc on parent of the current tag
    for node in element.iter():
        if node is not element:
            node.getparent().remove(node)

    res = u'\r\n'.join((
        word_wrap(text)
        for text in paragraphs
    ))
    res = re.sub(MANY_LINE_ENDINGS, '\r\n\r\n', res)
    element.text = res


def word_wrap(text):
    """
    Splits text with \r\n. Max symbols 80. Word wrap.
    :param text: basestring
    :return: unicode
    """
    if not isinstance(text, basestring):
        raise TypeError('text parameter has to be basestring instance')
    text = del_trash_symbols(text)
    if len(text) <= 80:
        return u''.join((text, u'\r\n'))
    lines = []
    while len(text) > 80:
        last_space = text[:80].rfind(' ')

        # if word large then 80 symbols
        if last_space == -1:
            last_space = text.find(' ')
        if last_space == -1:
            break

        line, text = text[:last_space], text[last_space+1:]
        lines.append(line)

    lines.append(text)
    lines.append('\r\n')
    return u'\r\n'.join(lines)

