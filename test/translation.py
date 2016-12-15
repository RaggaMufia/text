from text.torchtext import data
from text.torchtext import datasets

import re
import spacy

spacy_de = spacy.load('de')
spacy_en = spacy.load('en')

url = re.compile('(<url>.*</url>)')

def tokenize_de(text):
    return [tok.text for tok in spacy_de.tokenizer(url.sub('@URL@', text))]

def tokenize_en(text):
    return [tok.text for tok in spacy_en.tokenizer(url.sub('@URL@', text))]


DE = data.Field(time_series=True, tokenize=tokenize_de)
EN = data.Field(time_series=True, tokenize=tokenize_en)

train, dev = datasets.TranslationDataset.splits(
    path='~/iwslt2016/de-en/', train='train.tags.de-en',
    dev='IWSLT16.TED.tst2013.de-en', exts=('.de', '.en'), fields=(DE, EN))

print(train.fields)
print(len(train))
print(vars(train[0]))
print(vars(train[100]))

train_iter, dev_iter = data.BucketIterator.splits(
    (train, dev), batch_size=3, device=0)

DE.build_vocab(train.src, min_freq=3)
EN.build_vocab(train.trg, max_size=50000)

print(DE.vocab.freqs.most_common(10))
print(DE.vocab.size)
print(EN.vocab.freqs.most_common(10))
print(EN.vocab.size)

batch = next(iter(train_iter))
print(batch.src)
print(batch.trg)
