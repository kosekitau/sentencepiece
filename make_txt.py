import pandas as pd
import unicodedata
import re


def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFKC', s)
    )

def normalizeString(text):
    s = unicodeToAscii(text.lower().strip())
    s = re.sub(r"([.!?])", r"\1", s)
    s = re.sub(r"\s+", r" ", s).strip()
    s = re.sub(r'[【】]', '', s)                  # 【】の除去
    s = re.sub(r'[（）()]', '', s)                # （）の除去
    s = re.sub(r'[［］\[\]]', '', s)              # ［］の除去
    s = re.sub(r'[\r]', '', s)
    s = re.sub(r'　', ' ', s)                    #全角空白の除去
    s = re.sub(r'req:', '', s)
    s = re.sub(r'res:', '', s)
    s = re.sub(r'[^a-zA-Zぁ-んァ-ン一-龥0-9、。,.!?ー ]', '', s)
    return s

def make(path):
    with open(path + '.txt') as f:
        #txtデータの読み込み
        data = f.readlines()
        result = list(dict.fromkeys([normalizeString(data[i]) for i in range(len(data))]))
        with open('pre.txt', mode='w') as g:
            g.write('\n'.join(result))


paths = ['tiu_twitter']
for path in paths:
    make(path)
