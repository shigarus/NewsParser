# -*- coding: utf-8 -*-

import codecs
import os

import grab
import lxml.html.diff as htmldiff
from lxml.etree import tostring
from lxml.html import parse


def write_result(somestr, fpath):
    with codecs.open(fpath, encoding='utf-8', mode='w') as fh:
        fh.write(somestr)


if __name__ == '__main__':
    out_dir = 'output'
    out_file = 'output.txt'
    out_path = os.path.join(out_dir, out_file)

    g = grab.Grab()
    g.go('http://lenta.ru/news/2015/09/05/gaz/')
    tree1 = g.doc.tree
    g.go('http://lenta.ru/news/2015/09/04/ready/')
    tree2 = g.doc.tree
    diff = htmldiff.htmldiff(tree1, tree2)
    write_result(diff, out_path)
    new_tree = parse(out_path)
    write_result(tostring(new_tree), out_path)
