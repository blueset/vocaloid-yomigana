#%%
import MeCab
from pyokaka import okaka
import csv
import jaconv
import unicodedata
import re

tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd --node-format="%M\t%f[7]\n" --unk-format="%M\t%M\n"')
prefix = "outcomes/fandom/fandom"

# %%
def romaji_to_hiragana(romaji):
    return strip_punct(okaka.convert(romaji))

# %%
rows = []
with open(prefix + '.csv', newline='') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in spamreader:
         rows.append(list(map(jaconv.normalize, row)))

# %%

def strip_punct(s):
    return ''.join(c for c in jaconv.normalize(s) if unicodedata.category(c)[0] == 'L')

# %%
def kata_to_hira(s):
    return ''.join(map(jaconv.kata2hira, s))

# %%
kana_pattern = re.compile(r'^[\u3041-\u3096\u30A1-\u30FAー]*$')
def all_kana(s):
    return kana_pattern.match(strip_punct(s)) is not None
# %%
hira_pattern = re.compile(r'[\u3041-\u3096]+')
def find_all_hiragana(s):
    return hira_pattern.findall(strip_punct(s))
# %%
hira_kan_pattern = re.compile(r'^[\u3041-\u3096々〇〻\u3400-\u9FFF\uF900-\uFAFF]+$')
def all_hira_kan(s):
    return hira_kan_pattern.match(strip_punct(s)) is not None
# %%
def construct_kana(orig):
    r = list(map(lambda a: a.split("\t"), tagger.parse(orig).split('\n')))[:-2]
    return r, "".join(map(lambda a: a[1], r))
#%%
def sort_name(romaji, orig):
    if all_kana(strip_punct(orig)):
        return strip_punct(kata_to_hira(orig)), "safe"

    recovered = romaji_to_hiragana(romaji)
    if not recovered or not all_kana(recovered):
        recovered = None
    
    matching = recovered is not None

    constructed_pairs, constructed = construct_kana(orig)
    constructed = strip_punct(kata_to_hira(constructed))

    if not all_hira_kan(kata_to_hira(strip_punct(orig))):
        return constructed, "review"

    if recovered is not None:
        for kan, kata in constructed_pairs:
            hira = kata_to_hira(kata)
            if all_hira_kan(kan):
                print("matching", hira, "in", recovered)
                matching = matching and hira in recovered
        return constructed, "safe" if matching else "review"
    else:
        return constructed, "review"
# %%
with_romaji = [i for i in rows if i[0]]
without_romaji = [i for i in rows if not i[0]]

# %%
to_review = []
no_romaji_to_review = []
safe = []

for romaji, orig in with_romaji:
    kana, status = sort_name(romaji, orig)
    if status == "safe":
        safe.append((romaji, orig, kana))
    elif status == "review":
        to_review.append((romaji, orig, kana))

for romaji, orig in without_romaji:
    kana, status = sort_name(romaji, orig)
    if status == "safe":
        safe.append((romaji, orig, kana))
    elif status == "review":
        no_romaji_to_review.append((romaji, orig, kana))
# %%
def write_csv(data, fn):
    with open(fn, 'w', newline='') as csvfile:
        writter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in data:
            writter.writerow(i)
# %%
write_csv(safe, prefix + "_safe.csv")
write_csv(to_review, prefix + "_to_review.csv")
write_csv(no_romaji_to_review, prefix + "_no_romaji_to_review.csv")
# %%
