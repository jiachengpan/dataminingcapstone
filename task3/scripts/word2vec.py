#! /usr/bin/env python2

import sys
import gensim
import logging

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Sentences(object):
    stops = stopwords.words('english')
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with open(self.path) as fh:
            self.cnt = 0
            for line in fh:
                self.cnt += 1
                if self.cnt > 10000: break
                line = line.strip().decode('utf-8')
                for sent in sent_tokenize(line):
                    yield [i.lower() for i in word_tokenize(sent) if i.lower() not in Sentences.stops]


def proceeseLabel(path):
    pos = []
    neg = []
    with open(path) as fh:
        for line in fh:
            token, label = line.strip().split('\t')
            token = '_'.join(token.split())
            if int(label):
                pos.append(token)
            else:
                neg.append(token)
    return (pos, neg)

if __name__ == '__main__':
    if sys.argv[1] == 'train':
        # train
        inputPath = sys.argv[2]
        modelPath = sys.argv[3]

        sentences = Sentences(inputPath)
        model = gensim.models.Word2Vec(sentences, workers=6)
        model.save(modelPath)

    elif sys.argv[1] == 'train_phrase':
        inputPath = sys.argv[2]
        modelPath = sys.argv[3]
        ngramNum = int(sys.argv[4])

        sentences = Sentences(inputPath)

        ngram = None
        for i in range(ngramNum - 1):
            ngram = gensim.models.Phrases(sentences)
            print 'a'

        model = gensim.models.Word2Vec(ngram[sentences], workers=6)
        model.save(modelPath)

    elif sys.argv[1] == 'analyse':
        modelPath = sys.argv[2]
        model = gensim.models.Word2Vec.load(modelPath)


        labelPath = sys.argv[3]
        labelpos, labelneg = proceeseLabel(labelPath)

        labelpos = set(labelpos) & set(model.vocab.keys())
        labelneg = set(labelneg) & set(model.vocab.keys())

        mostSim = model.most_similar(
                positive=labelpos,
                negative=labelneg,
                topn=100000
                )

        newDishes = [i[0] for i in mostSim if len(i[0].split('_')) > 1]
        for dish in list(newDishes)[:20]:
            print dish

