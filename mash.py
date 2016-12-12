# from urllib2 import urlopen
# import xml.etree.ElementTree as ET
# dictUrl = 'http://services.aonaware.com/DictService/DictService.asmx/DefineInDict?dictId=gcide&word='
# namespace = '{http://services.aonaware.com/webservices/}'
# def getPast(verb):
#     xml = urlopen(dictUrl + verb).read()
#     print xml
#     tree = ET.fromstring(xml)
#     print tree[1]
#     text = ''
#     for node in tree.iter(namespace + 'WordDefinition'):
#         text = node.text
#         if len(node.text) > 5:  # real def, not start tag
#             text = node.text
#             break
#     i = text.find('[imp. {')
#     return text

# getPast('run')  # old api stuff
from random import sample, randint, choice
import api.text_processing as textproc
import re
import os
import sys
from collections import Counter

def gen_ngrams(text, n):
    wordsplit = [i.strip() for i in text.split(' ')]
    repeatntext = [wordsplit[i:] for i in range(n)]  # 'abcde', 'bcde', 'cde'
    return Counter([tuple(i) for i in zip(*repeatntext)])  # pass this as args, 'abc', 'bcd, 'cde'

def with_begin(lessgram, fullgram):
    l = len(lessgram)
    newc = Counter()
    for gram, count in fullgram.most_common():
        if gram[:l] == lessgram:
            newc[gram] = count
    return newc

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # no buffer
    with open('dictionaries/bibleform.txt') as f:
        text = f.read()
    bibgrams = gen_ngrams(text, 4)
    print 'gen done'
    gram, _ = bibgrams.most_common()[0]
    while 1:
        print gram[0],
        gram = choice(with_begin(gram[1:], bibgrams).most_common())[0]
