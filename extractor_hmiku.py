#%%
import json
import csv
import re
with open("meta.json", "r") as f:
    meta = json.load(f)

# %%
result = []
pattern = re.compile(r"&furigana\(([^\)]+?)\)")
for key, value in meta["meta"].items():
    name = value["name"]
    with open(key + ".wiki", "r") as f:
        text = f.read()
    match = pattern.search(text)
    yomigana = match.group(1) if match else ""
    if yomigana == "clear":
        yomigana = ""
    result.append((name, yomigana))
        

# %%
with open("hmiku.csv", 'w', newline='') as csvfile:
    writter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in result:
        writter.writerow(i)
# %%
