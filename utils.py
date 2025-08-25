import unicodedata

def norm(s:str)->str:
    s = s.strip().lower()
    s = ''.join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = s.replace("\n"," ").replace("\t"," ")
    s = s.replace("  "," ")
    return s