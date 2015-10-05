#! /usr/bin/env python2

import json
import os
import logging

class IndexYelpReviews():
    OUTPUT      = 'output'
    RESOURCE    = 'resource'

    def __init__(self):
        if not os.path.isdir(IndexYelpReviews.OUTPUT):
            raise Exception('Please generate %s directory first!' % ProcessYelp.OUTPUT)

    def load_reviews(self, category):
        self.reviews = []

        path = os.path.join(IndexYelpReviews.OUTPUT, 'categories', category)

        with open(path) as fh:
            for line in fh.readlines():
                if not line: break
                self.reviews.append({'text': line.strip()})

        with open(path + '.review_info') as fh:
            lineno = 0
            for line in fh.readlines():
                if not line: break
                rate, vote, rest = line.split('\t')
                vote = json.loads(vote)
                self.reviews[lineno]['rate'] = rate
                self.reviews[lineno]['vote'] = vote
                self.reviews[lineno]['rest'] = rest

    def index_dish2review(self, dish_path):
        dish2review = {}
        with open(dish_path) as fh:
            for line in fh.readlines():
                dish = line.strip()
                dish2review[dish] = []

        for idx, review in enumerate(self.reviews):
            text = review['text'].lower()
            for dish in dish2review:
                if dish not in text: continue
                dish2review[dish].append(idx)

        with open(os.path.join(IndexYelpReviews.OUTPUT, 'dish2review'), 'w') as fh:
            for dish, review in dish2review.items():
                fh.write('%s\t%s\n' % (dish, ' '.join([str(i) for i in review])))


if __name__ == '__main__':
    indexer = IndexYelpReviews()
    indexer.load_reviews('Chinese')
    #indexer.index_dish2review('./resource/chinese_dn_annotations.txt')
    indexer.index_dish2review('./resource/student_dn_annotations.txt')

