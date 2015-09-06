# -*- coding: utf-8 -*-
import lxml.html


H_TAGS = ['h{}'.format(i) for i in range(1, 7)]
TAGS_TO_SEPARATE = H_TAGS + ['p', 'li', ]


def html_to_readable(element):
    """
    Rules:
        length - 80 symbols
        word wrap
        paragraphs and title separated by new line
        <a href='url'>sometext</a> transforms to sometext[url]

    :param element: lxml.etree.ElementTree
    :return: unicode
    """
    if not isinstance(element, lxml.html.HtmlElement):
        raise TypeError('element has to be lxml.html.HtmlElement instance')
    paragraphs = []
    cur_str = u''
    for node in element.iter():
        tag = node.tag
        text = node.text
        if tag == 'br' and paragraphs:
            paragraphs.append(cur_str)
            cur_str = u''
        if tag in ('script', 'noscript'):
            continue
        if not text:
            continue
        if tag in TAGS_TO_SEPARATE:
            paragraphs.append(cur_str)
            if tag != 'li':
                paragraphs.append(u'')
            cur_str = u''
        if tag == 'a':
            text = u''.join([
                text,
                u'[{}]'.format(node.get('href'))
            ])
        cur_str = ''.join([cur_str, text, node.tail])
    return u''.join([
        word_wrap(text)
        for text in paragraphs
    ])


def word_wrap(text):
    """
    Splits text with \n. Max symbols 80. Word wrap.
    :param text: basestring
    :return: unicode
    """
    if not isinstance(text, basestring):
        raise TypeError('text parameter has to be basestring instance')
    if len(text) <= 80:
        return u''.join([text, u'\n'])
    lines = []
    while len(text) > 80:
        last_space = text[:80].rfind(' ')
        line, text = text[:last_space], text[last_space+1:]
        lines.append(line)
    lines.append(text)
    lines.append('\n')
    return u'\n'.join(lines)

