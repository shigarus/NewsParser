# -*- coding: utf-8 -*-

import argparse
import codecs
import json
import logging
import os

import htmltoreadable
import toolkit


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

    url = toolkit.morph_url(url)

    dir_path = os.path.dirname(url)
    file_path = url

    has_extension = True in (
        file_path.endswith(ext)
        for ext in ('.html', '.shtml', '.php')
    )
    if has_extension:
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
    # parse args
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
    # /parse args

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # getting config
    if os.path.exists(args.config):
        with codecs.open(args.config, 'r', encoding='utf-8') as fh:
            config = json.load(fh)
    else:
        config = dict(
            urls=[],
            rules={}
        )

    # getting rules and urls for processing
    if args.url:
        url = args.url
        site_name = toolkit.get_site_name(url)
        if args.target:
            exclude = args.exclude
            rule = dict(
                include=[args.target, ],
                exclude=[exclude, ] if exclude else []
            )
            rules = {
                site_name: rule
            }
        else:
            rules = config['rules']
        urls = [url, ]
    else:
        rules = config['rules']
        urls = config['urls']

    # process urls
    text_extractor = htmltoreadable.HtmlTextExtractor(rules)
    for url in urls:
        text = text_extractor.get_text(url)
        write_to_file(url, text)


if __name__ == '__main__':
    main()
