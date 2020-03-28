# tagger.py
## Description
A Python program that tags a word's part of speech in a given text file based on the probability of a current tag and the previous tag. The model is calculated from training data which is just a pre-tagged file (pos-train.txt). Details of the model are in the comments of the file. 

## Installation
Run in terminal or via cmd-line with Python 3. I suggest STDOUT so you can view the tagged words in a separate text file. 

```bash
python3 tagger.py pos-train.text pos-test.txt > pos-test-with-tags.txt
```