# -*- coding: utf-8 -*-
import re

import lxml.html
import lxml.etree


H_TAGS = ['h{}'.format(i) for i in range(1, 7)]
TAGS_TO_SEPARATE = H_TAGS + ['p', 'li', ]

MANY_LINE_ENDINGS = re.compile('(\n|\r\n){3,}')
TRASH_SPACES = re.compile(' {2,}')
TRASH_SYMBOLS = re.compile('[\r\n\t]')


def del_trash_symbols(line):
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

    # need to process inner <a> tags
    # to avoid collisions with adding url after <a> tag
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

    inner_tags_to_text(element)
    return element.text


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

        # check if tag closes current paragraph
        tag = node.tag
        if tag == 'br':
            paragraphs.append(cur_str)
            cur_str = u''
        if tag in TAGS_TO_SEPARATE:
            paragraphs.append(cur_str)
            if tag != 'li':
                paragraphs.append(u'')
            cur_str = u''

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

