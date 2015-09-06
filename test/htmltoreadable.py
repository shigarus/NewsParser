# -*- coding: utf-8 -*-
import codecs
import os

import grab

from src import htmltoreadable as hr

if __name__ == '__main__':
    g = grab.Grab()
    g.go('http://lenta.ru/news/2015/09/06/lamafound/')
    root_node = g.css('.b-topic__content')
    text = hr.html_to_readable(root_node)
    path = 'out'
    if not os.path.exists(path):
        os.mkdir(path)
    outpath = os.path.join(path, 'out.log')
    with codecs.open(outpath, 'w', encoding='utf-8') as fh:
        fh.write(text)
