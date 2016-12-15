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
import re
import os
import sys
from collections import Counter
from api.reddit import init, getLotsOfCommentText as getComments

def check_tuple(tup):
    bad = ['fuck', 'shit', 'ass', '://']  # i like the fact that i had to do this
    for word in tup:
        for no in bad:
            if no in word:  # thats a no-no
                return False
    return True
def gen_ngrams(text, n, ctr=0, needssplit=True):
    if needssplit:
        wordsplit = [i.strip() for i in text.split(' ')]
    else:
        wordsplit = text
    repeatntext = [wordsplit[i:] for i in range(n)]  # 'abcde', 'bcde', 'cde'
    if ctr == 0:
        return Counter([tuple(i) for i in zip(*repeatntext)])  # pass this as args, 'abc', 'bcd, 'cde'
    else:
        for i in zip(*repeatntext):
            tup = tuple(i)
            if check_tuple(tup):
                ctr[tuple(i)] += 1
        return ctr

def with_begin(lessgram, fullgram):
    l = len(lessgram)
    newc = Counter()
    for gram, count in fullgram.most_common():
        if gram[:l] == lessgram:
            newc[gram] = count
    return newc

def formWords(gramdict, gram=0):
    ''' puts words together goodly
    gramdict - dictionary of grams
    gram - ngram of words to begin with, default is random
    '''
    if gram == 0:
        gram = choice(list(gramdict.elements()))
    gen = ''
    startwith = []
    i = 1
    while 1:
        startwith = [0]
        i = 0
        while(len(startwith) <= 1):  # at end, i is num of elements to be printed
            i += 1
            startwith = with_begin(gram[i:], gramdict)
            # print gram[i:], 'produced', len(startwith), 'matches'
        gen += ' '.join(gram[:i]) + ' '
        yield gen[:-1]  # trim final space
        gram = choice(list(startwith.elements()))
    yield gen[:-1]
        
def ngramFromComments(comments, n):
    counter = Counter()
    sep = chr(2)
    normalized = sep.join(comments) \
                    .replace('\t', ' ') \
                    .replace('\n', ' ') \
                    .lower() \
                    .split(sep)
    for comment in normalized:
        text = filter(None, comment.split(' '))
        gen_ngrams(text, n, counter, False)
    return counter

def ngramsFromSubreddits(sr1, sr2, n=4, maxcalls=30):
    comments1 = getComments(sr1, maxcalls / 2)
    comments2 = getComments(sr2, maxcalls / 2)
    grams = ngramFromComments(comments1, n) + ngramFromComments(comments2, n)
    return grams

def getComment(grams, minLen=200):
    for i in formWords(grams):
        if len(i) >= minLen:
            return i

def bibletest():
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # no buffer
    with open('dictionaries/bibleform.txt') as f:
        text = f.read()
    bibgrams = gen_ngrams(text, int(sys.argv[1]))
    it = formWords(bibgrams)
    n = 10
    for i in it:
        print i
        n -= 1
        if n == 0: break

def commenttest():
    with open('../dictionaries/hscomments') as f:
        hscomments = eval(f.read())
    with open('../dictionaries/polcomments') as f:
        polcomments = eval(f.read())
    gramdict = ngramFromComments(hscomments, 3) + ngramFromComments(polcomments, 3)
    for i in formWords(gramdict):
        print i.encode('utf-8')

def getMash(sub1, sub2, count = 1):
  ngrams = ngramsFromSubreddits(sub1, sub2, 3, 10);
  ret = []

  for i in range(count):
    ret.append(getComment(ngrams))

  return ret

if __name__ == '__main__':
    init()
    grams = ngramsFromSubreddits('politics', 'tf2')
    for _ in range(10):
        print getComment(grams).encode('utf-8')
