#! /usr/bin/env python2

import json
import os
import logging

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

stop = stopwords.words('english')

reviews = []
with open('./output/categories/Chinese') as fh:
    for line in fh.readlines():
        reviews.append(line.strip())

rate2reviews = []
with open('./output/categories/Chinese.review_info') as fh:
    lineno = 0
    for line in fh.readlines():
        rate = int(line.split()[0])
        review = reviews[lineno]
        lineno += 1

        if rate > 3:    rate = 'pos'
        elif rate < 3:  rate = 'neg'
        else:           continue

        for sent in sent_tokenize(review.decode('utf-8').lower()):
            rate2reviews.append((rate, sent))

        if len(rate2reviews) > 400: break

dish_names = []
with open('./resource/student_dn_annotations.txt') as fh:
    for line in fh.readlines():
        dish_names.extend(line.decode('utf-8').strip().split())

stop.extend(list(set(dish_names)))

with open('./output/sentiment_train', 'w') as fh:
    fh.write('\n'.join(['\t'.join([str(i) for i in row]) for row in rate2reviews]))

train = rate2reviews

from nltk.tokenize import word_tokenize # or use some other tokenizer
all_words = set(word.lower() for passage in train for word in word_tokenize(passage[1]) if word not in stop)
t = [({word: (word in word_tokenize(x[1])) for word in all_words}, x[0]) for x in train]

import nltk
classifier = nltk.NaiveBayesClassifier.train(t)
classifier.show_most_informative_features()

#import pickle
#
#f = open('output/classifier.pickle', 'wb')
#pickle.dump(classifier, f)
#f.close()
#
#f = open('output/classifier.allwords.pickle', 'wb')
#pickle.dump(all_words, f)
#f.close()
