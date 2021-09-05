# Vocaloid song title yomigana ボカロ曲名よみがなデータ

An incomplete list of Vocaloid song title yomigana data, based on the [database dump](https://github.com/blueset/vocaloid-database-dump) of Vocaloid Wiki on Fandom, 初音ミク Wiki (atwiki) and VocaDB, with 2171, 3500 and 82721 usable entries from each source.

## Python Source

**Note**: the source code used here is unorganised and could be improved.

* `extractor_*.py`: extractor script to get romaji/yomigana and song title from the data set.
* `sanitize_kana.py`: generate yomigana from romaji and verify it against that generated from the song title.
* `sort_non_ja`: try to filter out non-Japanese songs and songs with a mixed-language title.

## Dependencies

* [MeCab](https://taku910.github.io/mecab/)
* [MeCab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd)
* `pip3 install regex jaconv pyokaka mecab-python3`

---

> search keyword: vocaloid song names yomigana romaji furigana hiragana katakana kana pronunciation database ボカロ ボーカロイド 曲名 読み方 読み仮名 ひらがな カタカナ 仮名 よみがな

