# -*- coding: utf-8 -*-

import argparse
import codecs
import logging
import os

import grab

import htmltoreadable


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', dest='url')
    parser.add_argument('--target', dest='target')
    args = parser.parse_args()

    g = grab.Grab()
    g.go(args.url)
    tree = g.doc.tree
    target_element = tree.cssselect(args.target)
    text = htmltoreadable.html_to_readable(target_element[0])

    with codecs.open('out.txt', 'w', encoding='utf-8') as fh:
        fh.write(text)


if __name__ == '__main__':
    main()
