# -*- coding: utf-8 -*-
!pip install sentencepiece > /dev/null

import sentencepiece as spm

cd "/content/drive/My Drive/dataset/sentencepiece"

"""
spm.SentencePieceTrainer.Train(
    '--input=pre.txt, --model_prefix=sentencepiece_twitter --character_coverage=0.9995 --vocab_size=8000'
)
"""

sp = spm.SentencePieceProcessor()
sp.Load("sentencepiece_twitter.model")

sp.EncodeAsPieces("こんにちは、僕はゴリラです。")

import torchtext
from torchtext.data.utils import get_tokenizer

MAX_LENGTH = 30

#テキストに処理を行うFieldを定義
#fix_lengthはtokenの数
SRC = torchtext.data.Field(sequential=True, use_vocab=True, tokenize=sp.EncodeAsPieces,
                            lower=True, include_lengths=True, batch_first=True, fix_length=MAX_LENGTH,
                            eos_token='<eos>')

TRG = torchtext.data.Field(sequential=True, use_vocab=True, tokenize=sp.EncodeAsPieces,
                            lower=True, include_lengths=True, batch_first=True, fix_length=MAX_LENGTH,
                            init_token='<cls>', eos_token='<eos>')

train_ds, val_ds = torchtext.data.TabularDataset.splits(
    path='/content/drive/My Drive/dataset/TIU/twitter/5_20', train='train.csv', validation='val.csv',
    format='csv', fields=[('src', SRC), ('trg', TRG)])

SRC.build_vocab(train_ds)
TRG.build_vocab(train_ds)
print(TRG.vocab.stoi)
print(len(TRG.vocab.stoi))

from torchtext import data

batch_size = 128

train_dl = data.Iterator(train_ds, batch_size=batch_size, train=True)
val_dl = data.Iterator(val_ds, batch_size=batch_size, train=False, sort=False)
batch = next(iter(val_dl))
print(batch.trg[0])
