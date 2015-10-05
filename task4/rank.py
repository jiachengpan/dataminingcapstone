#! /usr/bin/env python2

import json
import os
import logging
import math
import pprint
import pickle

from nltk.tokenize import sent_tokenize, word_tokenize
import nltk


class RankYelpDishes():
    OUTPUT      = 'output'
    RESOURCE    = 'resource'

    def __init__(self, category):
        self.rest_id2rest_name = {}
        with open(os.path.join(RankYelpDishes.OUTPUT, 'rest_id2rest_name.json')) as fh:
            self.rest_id2rest_name = json.load(fh)

        self.reviews = []
        path = os.path.join(RankYelpDishes.OUTPUT, 'categories', category)

        with open(path) as fh:
            for line in fh.readlines():
                if not line: break
                self.reviews.append({'text': line.strip()})

        with open(path + '.review_info') as fh:
            lineno = 0
            for line in fh.readlines():
                if not line: continue
                rate, vote, rest = line.strip().split('\t')
                vote = json.loads(vote)
                self.reviews[lineno]['rate'] = rate
                self.reviews[lineno]['vote'] = vote
                self.reviews[lineno]['rest'] = rest
                lineno += 1

        self.dish2review = {}
        with open(os.path.join(RankYelpDishes.OUTPUT, 'dish2review')) as fh:
            for line in fh.readlines():
                dish, reviews = line.split('\t')
                reviews = reviews.strip()
                if not reviews: continue
                self.dish2review[dish] = []
                for review in reviews.split():
                    self.dish2review[dish].append(self.reviews[int(review)])

        with open('output/classifier.pickle') as fh:
            self.classifier = pickle.load(fh)

        with open('output/classifier.allwords.pickle') as fh:
            self.allwords = pickle.load(fh)

        #with open(os.path.join(RankYelpDishes.OUTPUT, 'dish2review.json'), 'w') as fh:
        #    json.dump(self.dish2review, fh, indent=2)

    def __sentiment(self, test_sentence):
        test_sent_features = { word.lower(): (word in word_tokenize(test_sentence.lower())) for word in self.allwords }
        ret = self.classifier.classify(test_sent_features)
        if ret == 'pos':
            return 1
        else:
            return -1

    def rank_by_sentiment(self):
        dish2sent = {}
        cnt = 0
        cnt_all = len(self.dish2review.keys())
        for dish, reviews in self.dish2review.items():
            if cnt % 10 == 0: print cnt, cnt_all
            cnt += 1
            dish2sent[dish] = []
            for idx, review in enumerate(reviews):
                for sent in sent_tokenize(review['text'].decode('utf-8').lower()):
                    if dish not in sent: continue
                    score = self.__sentiment(sent)
                    dish2sent[dish].append((sent, score))

        dish_ranks = []
        # compute dish ranking
        for dish, sents in dish2sent:
            score = 0
            for sent in sents:
                score += sent[1]
            if len(sents):
                score = float(score) / len(sents)
            dish_ranks.append({
                'name': dish,
                'score': score,
                'freq': len(sents),
                })

        dish_ranks.sort(key=lambda x: x['freq'])

        with open(os.path.join(RankYelpDishes.OUTPUT, 'dish_rank_by_senti.json'), 'w') as fh:
            json.dump(dish_ranks, fh, indent=2)

        # compute restaurant ranking for top-20 dishes
        rest_ranks = {}
        for dish_info in dish_ranks[-20:]:
            dish = dish_info['name']
            rest_ranks[dish] = []

            rest2review = {}
            reviews = self.dish2review[dish]
            for review in reviews:
                if review['rest'] not in rest2review:
                    rest2review[review['rest']] = []
                rest2review[review['rest']].append(review)

            for rest, reviews in rest2review.items():
                score = 0
                denom = 0
                for review in reviews:
                    for sent in sent_tokenize(review['text'].decode('utf-8').lower()):
                        if dish not in sent: continue
                        score += self.__sentiment(sent)
                        denom += 1

                if denom == 0:
                    score = 0
                else:
                    score = float(score) / denom

                rest_ranks[dish].append({
                    'name': self.rest_id2rest_name[rest],
                    'score': score,
                    'freq': denom
                    })
            rest_ranks[dish].sort(key=lambda x: x['freq'])

        with open(os.path.join(RankYelpDishes.OUTPUT, 'dish_rank_by_senti.json'), 'w') as fh:
            json.dump(dish_ranks, fh, indent=2)

        #with open(os.path.join(RankYelpDishes.OUTPUT, 'rest_rank_by_senti.json'), 'w') as fh:
        #    json.dump(rest_ranks, fh, indent=2)


    def rank_by_ratings(self):
        # dish_name, rank_score, review_occurrence
        dish_ranks = []
        # compute dish ranking
        for dish, reviews in self.dish2review.items():
            score = 0
            denom = 0
            for review in reviews:
                denom += 1
                score += int(review['rate'])
                if review['vote']['useful'] > 0:
                    denom += review['vote']['useful']
                    score += review['vote']['useful'] * int(review['rate'])
            if denom == 0:
                score = 0
            else:
                score = float(score) / denom
            score *= math.log(1 + len(reviews))
            dish_ranks.append({
                'name': dish,
                'score': score,
                'freq': len(reviews)
                })

        dish_ranks.sort(key=lambda x: x['freq'])

        # compute restaurant ranking for top-20 dishes
        rest_ranks = {}
        for dish_info in dish_ranks[-20:]:
            dish = dish_info['name']
            rest_ranks[dish] = []

            rest2review = {}
            reviews = self.dish2review[dish]
            for review in reviews:
                if review['rest'] not in rest2review:
                    rest2review[review['rest']] = []
                rest2review[review['rest']].append(review)

            for rest, reviews in rest2review.items():
                score = 0
                denom = 0
                for review in reviews:
                    denom += 1
                    score += int(review['rate'])
                    if review['vote']['useful'] > 0:
                        denom += review['vote']['useful']
                        score += review['vote']['useful'] * int(review['rate'])
                if denom == 0:
                    score = 0
                else:
                    score = float(score) / denom
                score *= math.log(1 + len(reviews))

                rest_ranks[dish].append({
                    'name': self.rest_id2rest_name[rest],
                    'score': score,
                    'freq': len(reviews)
                    })
            rest_ranks[dish].sort(key=lambda x: x['freq'])

        with open(os.path.join(RankYelpDishes.OUTPUT, 'dish_rank_by_ratings.json'), 'w') as fh:
            json.dump(dish_ranks, fh, indent=2)

        with open(os.path.join(RankYelpDishes.OUTPUT, 'rest_rank_by_ratings.json'), 'w') as fh:
            json.dump(rest_ranks, fh, indent=2)

if __name__ == '__main__':
    ranker = RankYelpDishes('Chinese')
    #ranker.rank_by_ratings()
    ranker.rank_by_sentiment()


