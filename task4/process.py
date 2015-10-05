#! /usr/bin/env python2

import json
import os
import logging

class ProcessYelp():
    R = 'Restaurants'
    CAT_SAMPLE = 0

    OUTPUT = 'output'

    def __init__(self):
        self.cat2rest       = {}
        self.rest2rate      = {}
        self.rest2cat       = {}
        self.rest2review    = {}
        self.rest2review_rate   = {}
        self.rest2review_vote   = {}
        self.bu_id2bu_name  = {}


        if os.path.isdir(ProcessYelp.OUTPUT) or os.path.isfile(ProcessYelp.OUTPUT):
            raise Exception('Please purge %s directory first!' % ProcessYelp.OUTPUT)

        os.mkdir(ProcessYelp.OUTPUT)

    def get_restaurants(self, path):
        logging.info('Getting restaurant information')
        with open(path) as fh:
            for line in fh.readlines():
                business_json = json.loads(line)
                categories = business_json['categories']

                # is a restaurant and more than a restaurant
                if ProcessYelp.R in categories and len(categories) > 1:
                    rest_id = business_json['business_id']
                    rest_star = business_json['stars']

                    categories = set(categories) - set([self.R])

                    if rest_id in self.rest2cat: raise Exception('Duplicate restaurant!')

                    self.bu_id2bu_name[rest_id] = business_json['name']
                    self.rest2cat[rest_id] = categories
                    self.rest2rate[rest_id] = rest_star

                    # for restaurants' review data
                    self.rest2review[rest_id] = []
                    self.rest2review_rate[rest_id] = []
                    self.rest2review_vote[rest_id] = []

                    for c in categories:
                        if c not in self.cat2rest: self.cat2rest[c] = []
                        self.cat2rest[c].append(rest_id)

    def get_reviews(self, path):
        logging.info('Getting review information')
        cat2review_count = {c: 0 for c in self.cat2rest}
        with open(path) as fh:
            for line in fh.readlines():
                review_json = json.loads(line)
                review_bu_id    = review_json['business_id']
                review_text     = review_json['text']
                review_stars    = review_json['stars']
                review_votes    = review_json['votes']

                # dump non-restaurant reviews
                if review_bu_id not in self.rest2cat: continue

                self.rest2review[review_bu_id].append(review_text.replace('\n', ' ').strip())
                self.rest2review_rate[review_bu_id].append(str(review_stars))
                self.rest2review_vote[review_bu_id].append(json.dumps(review_votes))

                for c in self.rest2cat[review_bu_id]:
                    cat2review_count[c] += 1

        # dump invalid categories
        invalid_categories = [c[0] for c in sorted(cat2review_count.items(), key=lambda x: x[1])][:-self.CAT_SAMPLE]
        for cat in invalid_categories:
            del self.cat2rest[cat]


    def write_cat2review(self):
        output_dir = os.path.join(ProcessYelp.OUTPUT, 'categories')
        os.mkdir(output_dir)

        for cat in self.cat2rest:
            reviews = []
            review_rates = []
            review_votes = []
            review_rests = []
            for rest_id in self.cat2rest[cat]:
                reviews.extend(self.rest2review[rest_id])
                review_rates.extend(self.rest2review_rate[rest_id])
                review_votes.extend(self.rest2review_vote[rest_id])
                review_rests.extend([rest_id] * len(self.rest2review[rest_id]))

            cat = cat.replace('/', '-').replace(' ', '_')
            with open(os.path.join(output_dir, cat), 'w') as fh:
                fh.write(u'\n'.join(reviews).encode('utf-8').strip())
            with open(os.path.join(output_dir, '%s.review_info' % cat), 'w') as fh:
                for i in range(len(review_rates)):
                    fh.write('\t'.join([review_rates[i], review_votes[i], review_rests[i]]))
                    fh.write('\n')

    def write_restaurants(self):
        with open(os.path.join(ProcessYelp.OUTPUT, 'rest_id2rest_name.json'), 'w') as fh:
            json.dump(self.bu_id2bu_name, fh)

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)

    path2files      = "yelp_dataset_challenge_academic_dataset"
    path2buisness   = os.path.join(path2files, "yelp_academic_dataset_business.json")
    path2reviews    = os.path.join(path2files, "yelp_academic_dataset_review.json")

    process = ProcessYelp()
    process.get_restaurants(path2buisness)
    process.get_reviews(path2reviews)

    process.write_cat2review()
    process.write_restaurants()

