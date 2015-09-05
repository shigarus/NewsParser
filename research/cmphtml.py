# -*- coding: utf-8 -*-

import codecs
import os

import grab
import lxml.html.diff as htmldiff


def write_result(somestr, basedir='output', fpath='output.txt'):
    with codecs.open(os.path.join(basedir, fpath), encoding='utf-8', mode='w') as fh:
        fh.write(somestr)


if __name__ == '__main__':
    g = grab.Grab()
    g.go('http://lenta.ru/news/2015/09/05/gaz/')
    tree1 = g.doc.tree
    g.go('http://lenta.ru/news/2015/09/04/ready/')
    tree2 = g.doc.tree
    diff = htmldiff.htmldiff(tree1, tree2)
    write_result(diff)