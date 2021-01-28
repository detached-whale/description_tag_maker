description_tag_maker
=============

### Introduction
---
**description_tag_maker** is a python script to make a description tag by extracting key sentences from text. **[TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)** and **[TextRank](http://www.aclweb.org/anthology/W04-3252)** are used.

### Usage
---
```
# Import Maker module
from desscription_tag_maker.maker import Maker

maker = Maker()

# Get the result
# maker.make(text, number of lines to return)
# maker.make_from_web(url, number of lines to return, tag, attributes)
sentences = maker.make_from_web(text, 3)
sentences = maker.make_from_web(url, 3, 'div', {'class': 'class_name'})

```
### Demo
---
Demo extracts key sentences from **[news](https://news.infoseek.co.jp/article/20180526hochi235/)** and write to 'result.txt'.
