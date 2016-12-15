def getValue(d, key):
  if key in d:
    return d[key]

  return None

def sanitize(s):
  return s.replace(u'\u2018', '\'').replace(u'\u2019', '\'')
