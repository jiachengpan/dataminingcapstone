#! /usr/bin/env python2

from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from gensim import models
from gensim import matutils
from scipy.spatial import distance
from scipy.sparse import csr_matrix

import math
import glob
import logging
import itertools
import json
import os

class AnalyseYelp():
    CAT_DATA_PATH = 'output/categories'

    def __init__(self, listfile='catlist.tsv'):
        self.cat2text = {}
        catlist = []
        if os.path.isfile(listfile):
            with open(listfile) as fh:
                catlist = fh.read().split('\n')
        else:
            catlist = glob.glob(AnalyseYelp.CAT_DATA_PATH + '/*')[:50]

        for item in catlist:
            if not item: continue
            cat = item.split('/')[-1]
            logging.info('cat: ' + cat)

            with open(item) as fh:
                self.cat2text[cat] = fh.read().split('\n')

    def _vectorise(self, vectoriser):
        cat_text = []
        cat_name = []
        for cat in sorted(self.cat2text.keys()):
            cat_text.append(' '.join(self.cat2text[cat]))
            cat_name.append(cat)

        logging.info('fit_transform begin')
        t0 = time()
        X = vectoriser.fit_transform(cat_text)
        logging.info('done in %fs' % (time() - t0))
        logging.info(X.shape)

        id2word = {}
        for i, word in enumerate(vectoriser.get_feature_names()):
            id2word[i] = word

        return (X, id2word, cat_name)

    def _vectorise_sep(self, vectoriser):
        cat_text = []
        cat_name = []
        cat_size = []
        for cat in sorted(self.cat2text.keys()):
            size = 0
            for idx in range(0, len(self.cat2text[cat]), 200):
                cat_text.append(' '.join(self.cat2text[cat][idx:idx + 200]))
                size += 1
            #cat_text.append(' '.join(self.cat2text[cat][cur_idx:]))
            cat_name.append(cat)
            cat_size.append(size)

        logging.info('fit_transform begin')
        t0 = time()
        X = vectoriser.fit_transform(cat_text)
        logging.info('done in %fs' % (time() - t0))
        logging.info(X.shape)

        id2word = {}
        for i, word in enumerate(vectoriser.get_feature_names()):
            id2word[i] = word

        return (X, id2word, cat_name, cat_size)

    def cat_sim_text_sep(self,
            compute_distance=distance.cosine,
            output='cat_sim_text_sep',
            norm='l1',
            use_idf=False,
            sublinear_tf=False,
            ):

        vectoriser = TfidfVectorizer(
                max_features= 10000,
                stop_words  = 'english',
                norm        = norm,
                use_idf     = use_idf,
                sublinear_tf= sublinear_tf,
                )
        X, id2word, cat_name, cat_size = self._vectorise_sep(vectoriser)

        cat2ids = []
        cur_id = 0
        for i in range(len(cat_name)):
            cat2ids.append(range(cur_id, cur_id + cat_size[i]))
            cur_id += cat_size[i]


        result = []
        for cat_a in range(len(cat_name)):
            print '%d / %d' % (cat_a, len(cat_name))
            for cat_b in range(cat_a, len(cat_name)):
                local_dist = []
                for pair in itertools.product(cat2ids[cat_a], cat2ids[cat_b]):
                    vec1 = X.getrow(pair[0]).toarray()
                    vec2 = X.getrow(pair[1]).toarray()
                    dist = compute_distance(vec1, vec2)
                    local_dist.append(dist)
                result.append((cat_a, cat_b, sum(local_dist) / len(local_dist)))
        with open('output/%s.json' % output, 'w') as fh:
            json.dump({
                'data': result,
                'meta': {
                    'categories': cat_name,
                    }
                }, fh)

    def cat_sim_text(self,
            compute_distance=distance.cosine,
            output='cat_sim_text',
            norm='l1',
            use_idf=False,
            sublinear_tf=False,
            ):

        vectoriser = TfidfVectorizer(
                max_features= 10000,
                stop_words  = 'english',
                norm        = norm,
                use_idf     = use_idf,
                sublinear_tf= sublinear_tf,
                )
        X, id2word, cat_name = self._vectorise(vectoriser)

        result = []
        for cat_a in range(X.shape[0]):
            for cat_b in range(cat_a, X.shape[0]):
                dist = compute_distance(
                        X.getrow(cat_a).toarray(),
                        X.getrow(cat_b).toarray())
                result.append((cat_a, cat_b, dist))

        with open('output/%s.json' % output, 'w') as fh:
            json.dump({
                'data': result,
                'meta': {
                    'categories': cat_name,
                    }
                }, fh)

    def cat_sim_bm25_idf_lda(self,
            compute_distance=distance.cosine,
            output='lda_tf_idf',
            ):
        vectoriser = TfidfVectorizer(
                max_df      = 0.5,
                min_df      = 2,
                max_features= 10000,
                stop_words  = 'english',
                use_idf     = True,
                sublinear_tf= True,
                )
        X, id2word, cat_name = self._vectorise(vectoriser)

        corpus = matutils.Sparse2Corpus(X, documents_columns=False)

        lda = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=id2word)
        doc_topics = lda.get_document_topics(corpus)

        # transform to sparse
        data = []
        cols = []
        rows = []
        for i, doc in enumerate(doc_topics):
            for term, weight in doc:
                data.append(weight)
                cols.append(term)
                rows.append(i)
        topic_mat = csr_matrix((data, (rows, cols)),
                shape=(X.shape[0], X.shape[1]))

        result = []
        # computing cosine similarity matrix
        for i in range(X.shape[0]):
            for j in range(i, X.shape[0]):
                dist = compute_distance(
                    topic_mat.getrow(i).toarray(),
                    topic_mat.getrow(j).toarray(),
                    )
                result.append((i, j, dist))

        with open('output/%s.json' % output, 'w') as fh:
            json.dump({
                'data': result,
                'meta': {
                    'categories': cat_name,
                    }
                }, fh)
        return 'output/%s.json' % output


    def _prepare_data_for_cluster(self, path):
        data = None
        with open(path) as fh:
            data = json.load(fh)
        dist = []
        cols = []
        rows = []
        for (row, col, val) in data['data']:
            dist.append(val)
            cols.append(col)
            rows.append(row)

            if row == col: continue

            dist.append(val)
            cols.append(row)
            rows.append(col)

        size = len(data['meta']['categories'])
        return (data, csr_matrix((dist, (rows, cols)), shape=(size, size)))

    def clustering_kmeans(self,
            path,
            n_clusters,
            ):
        cluster = KMeans(n_clusters=n_clusters)

        result, data = self._prepare_data_for_cluster(path)
        cluster.fit(data)
        result['cluster'] = cluster.labels_.tolist()
        with open(path, 'w') as fh:
            json.dump(result, fh)

    def clustering_agglomerative(self, path, n_clusters):
        cluster = AgglomerativeClustering(n_clusters=n_clusters)

        result, data = self._prepare_data_for_cluster(path)
        cluster.fit(data.toarray())
        result['cluster'] = cluster.labels_.tolist()
        with open(path, 'w') as fh:
            json.dump(result, fh)



if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)

    ana = AnalyseYelp(
            #'catlist_try.tsv'
            'catlist_countries.tsv'
            )
    #ana.cat_sim_text_sep(
    #        norm='l2',
    #        output='text_repr')
    #ana.cat_sim_text()
    #ana.cat_sim_text(
    #        norm='l2',
    #        output='text_repr')
    #ana.clustering_kmeans('./output/text_repr.json', 3)
    #ana.cat_sim_text(
    #        norm='l2',
    #        use_idf=True,
    #        sublinear_tf=True,
    #        output='text_repr_tf_idf')
    #ana.clustering_kmeans('./output/text_repr_tf_idf.json', 3)
    #path = ana.cat_sim_bm25_idf_lda(
    #        output='lda_tf_idf',
    #        )
    #ana.clustering_kmeans(path, 3)
    #ana.clustering_kmeans('./output/cluster_3.json', 3)
    #ana.clustering_kmeans('./output/cluster_6.json', 6)
    #ana.clustering_kmeans('./output/cluster_9.json', 9)
    ana.clustering_agglomerative('./output/hierarchical_3.json', 3)
    ana.clustering_kmeans('./output/cluster_3.json', 3)

