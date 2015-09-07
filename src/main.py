# -*- coding: utf-8 -*-

import argparse
import codecs
import logging
import os

import grab

import htmltoreadable


def write_to_file(url, text):
    """
    Write text to path like
        http://default.ru/news/2013/03/dtp/index.html => [CUR_DIR]/default.ru/news/2013/03/dtp/index.txt
    :param url: basestring
    :param text: basestring
    """
    if not isinstance(url, basestring):
        raise TypeError('url has to be basestring instance')
    if not isinstance(text, basestring):
        raise TypeError('text has to be basestring instance')

    if url.startswith('http://'):
        url = url[7:]
    if url.endswith('/'):
        url = url[:-1]

    dir_path = os.path.dirname(url)
    file_path = url

    if file_path.endswith('.html') or file_path.endswith('.php'):
        point_pos = file_path.rfind('.')
        file_path = file_path[:point_pos]
    file_path = u''.join((
        file_path,
        '.txt'
    ))

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with codecs.open(file_path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Target page url')
    parser.add_argument(
        '-t',
        '--target',
        help='Css selector to process text.'
    )
    args = parser.parse_args()

    g = grab.Grab()
    g.go(args.url)
    tree = g.doc.tree
    target_element = tree.cssselect(args.target)
    text = htmltoreadable.html_to_readable(target_element[0])

    write_to_file(args.url, text)


if __name__ == '__main__':
    main()
