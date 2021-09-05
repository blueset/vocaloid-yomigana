# %%
from lxml import etree
import glob
paths = glob.glob("Songs/*.xml")
#%%
def get_name_romaji(fn):
    lines = []
    root = etree.parse(fn)
    for song in root.findall(".//ArchivedSongContract"):
        skip = False
        if song.find(".//Lyrics/LyricsForSongContract") is not None:
            for lyrics in song.findall(".//Lyrics/LyricsForSongContract"):
                if lyrics.find(".//TranslationType").text == "Orignal" and \
                    lyrics.find(".//CultureCode").text != "ja":
                    skip = True
                    break
        if skip:
            continue
        j = song.find(".//TranslatedName/Japanese")
        r = song.find(".//TranslatedName/Romaji")
        jn = j.text if j is not None else None
        rn = r.text if r is not None and r.text != jn else None
        lines.append((jn, rn))
    return lines
# %%
lines = []
for path in paths:
    lines.extend(get_name_romaji(path))
# %%
import csv
with open('vocadb.csv', 'w', newline='') as csvfile:
    writter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in lines:
        writter.writerow(i[::-1])

# %%
