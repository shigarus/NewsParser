# -*- coding: utf-8 -*-
import codecs
import os

import grab

from src import htmltoreadable as hr


def test():
    g = grab.Grab()
    g.go('http://habrahabr.ru/post/266293/')
    root_node = g.css('.post_show')
    text = hr.html_to_readable(root_node)
    path = 'out'
    if not os.path.exists(path):
        os.mkdir(path)
    outpath = os.path.join(path, 'out.log')
    with codecs.open(outpath, 'w', encoding='utf-8') as fh:
        fh.write(text)


if __name__ == '__main__':
    test()

