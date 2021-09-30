#%%
import json
import csv
import re
import glob
import tqdm
import frontmatter

#%%
files = glob.glob("data/*.txt")


# %%
result = []
pattern = re.compile(r"&furigana\(([^\)]+?)\)")
for file in tqdm.tqdm(files):
    p = frontmatter.load(file)
    name = p["title"]
    text = p.content
    match = pattern.search(text)
    yomigana = match.group(1) if match else ""
    if yomigana == "clear":
        yomigana = ""
    if yomigana:
        result.append((name, yomigana))
        

# %%
with open("hmiku.csv", 'w', newline='') as csvfile:
    writter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in result:
        writter.writerow(i)
# %%