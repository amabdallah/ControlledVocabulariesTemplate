import re

def upper_splitted(string):
    return " ".join(re.findall('[A-Z][a-z]*', string))

lfirst = lambda s: s[:1].lower() + s[1:] if s else ''