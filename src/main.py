# -*- coding: utf-8 -*-

import argparse
import codecs
import json
import logging
import os

import grab

import htmltoreadable


def get_site_name(url):
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


def write_to_file(url, text):
    """
    Write text to path like
        default.ru/news/2013/03/dtp/index.html => [CUR_DIR]/default.ru/news/2013/03/dtp/index.txt
    :param url: basestring
    :param text: basestring
    """
    if not isinstance(url, basestring):
        raise TypeError('url has to be basestring instance')
    if not isinstance(text, basestring):
        raise TypeError('text has to be basestring instance')

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
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--url', help='Target page url')
    parser.add_argument(
        '-t',
        '--target',
        help='Css selector to process text.'
    )
    parser.add_argument(
        '-e',
        '--exclude',
        help='Css selector to exclude text.'
    )
    parser.add_argument('-c', '--config', help='Path to config file')
    parser.add_argument('-d', '--debug', action='store_true')

    parser.set_defaults(
        debug=False,
        config='config.json',
        exclude=None
    )
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if os.path.exists(args.config):
        with codecs.open(args.config, 'r', encoding='utf-8') as fh:
            config = json.load(fh)
    else:
        config = dict(
            urls=[],
            rules={}
        )

    if args.url:
        url = morph_url(args.url)
        site_name = get_site_name(url)
        if args.target:
            exclude = args.exclude
            rule = dict(
                include=[args.target, ],
                exclude=[exclude, ] if exclude else []
            )
        else:
            rule = config['rules'].get(site_name)
        rule_for_url = {
            url: rule
        }
    else:
        rule_for_url = {}
        for url in config['urls']:
            url = morph_url(url)
            site_name = get_site_name(url)
            rule_for_url[url] = config['rules'][site_name]

    g = grab.Grab()

    for url, rule in rule_for_url.items():
        g.go('http://'+url)
        target = rule['include'][0]
        tree = g.doc.tree
        target_element = tree.cssselect(target)
        text = htmltoreadable.html_to_readable(target_element[0])
        write_to_file(url, text)


if __name__ == '__main__':
    main()
