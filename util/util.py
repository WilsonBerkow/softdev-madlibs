import unicodedata

def getValue(d, key):
  if key in d:
    return d[key]

  return None

def sanitize(s):
  simple_quotes = s.replace(u'\u2018', '\'').replace(u'\u2019', '\'').replace(u'\u201d', '"').replace(u'\u201c', '"')
  all_ascii = simple_quotes.encode('ascii', 'ignore')
  return all_ascii
