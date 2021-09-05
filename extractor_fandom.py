#%%
from lxml import etree
root = etree.parse("./vocaloid_pages_current.xml")
# %%
ns = {None: "http://www.mediawiki.org/xml/export-0.10/"}
pages = root.findall(".//page", ns)
print(len(pages))
# %%
pages_with_song_box = []
for page in pages:
    rtext = page.find(".//revision/text", ns)
    if rtext.text and "Song box" in rtext.text: #int(rtext.attrib["bytes"]) > 10240:# "Song box 2" in rtext.text:
        pages_with_song_box.append(rtext.text)
#%%
def parse_brackets(text, lvl=0):
    result = []
    while text:
        first_open = text.find("{{")
        first_close = text.find("}}")
        beh = ""
        if first_open >= 0 and first_close >= 0:
            if first_open < first_close or lvl == 0:
                beh = "open"
            else:
                beh = "close"
        elif first_open >= 0:
            beh = "open"
        elif first_close >= 0 and lvl > 0:
            beh = "close"
        else:
            beh = "out"
        if beh == "open":
            before = text[:first_open]
            content = text[first_open + 2:]
            result.append(before)
            outcome, remainder = parse_brackets(content, lvl + 1)
            result.append(outcome)
            text = remainder
        elif beh == "close":
            content = text[:first_close]
            remainder = text[first_close+2:]
            result.append(content)
            return result, remainder
        else:
            result.append(text)
            text = ""
    return result, text
#%%
def get_song_box(parsed):
    for i in parsed:
        if type(i) == str:
            if "Song box" in i:
                return parsed
        else:
            v = get_song_box(i)
            if v:
                return v

#%%
parsed_boxes = []
for p in pages_with_song_box:
    if "{{" not in p or "Song box 2" not in p:
        continue
    # pp = p[p.find("{{"):]
    pp = parse_brackets(p)[0]
    l = get_song_box(pp)
    if not l:
        raise ValueError(pp)
    parsed_boxes.append(l)
# %%
import re
#%%
rmjre = re.compile("Romaji: *(.+?)\n")
title_re = re.compile("""\| *title *= *"?(?:''')?(.+?)(?:''')?"?\n""")

def extract_romaji(parsed, pattern):
    for i in parsed:
        if type(i) == str:
            m = pattern.search(i)
            if m:
                return m.group(1)
        else:
            v = extract_romaji(i, pattern)
            if v:
                return v

# %%
rmj_ttl = []
for i in parsed_boxes:
    rmj_ttl.append((extract_romaji(i, rmjre), extract_romaji(i, title_re)))

# %%
import csv
with open('vocaloid_fandom.csv', 'w', newline='') as csvfile:
    writter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in rmj_ttl:
        writter.writerow(i)
# %%
