import logging
import glob
import argparse
from gensim import models
from gensim import matutils
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
from nltk.tokenize import sent_tokenize

import json

def main(K, numfeatures, sample_file, num_display_words, outputfile):
    K_clusters = K
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=numfeatures,
                                     min_df=2, stop_words='english',
                                     ngram_range=(1, 2),
                                     use_idf=True)

    text = []
    with open (sample_file, 'r') as f:
        text = f.readlines()

    t0 = time()
    print("Extracting features from the training dataset using a sparse vectorizer")
    X = vectorizer.fit_transform(text)
    print("done in %fs" % (time() - t0))
    print("n_samples: %d, n_features: %d" % X.shape)

    # mapping from feature id to acutal word
    id2words ={}
    for i,word in enumerate(vectorizer.get_feature_names()):
        id2words[i] = word

    t0 = time()
    print("Applying topic modeling, using LDA")
    print(str(K_clusters) + " topics")
    corpus = matutils.Sparse2Corpus(X,  documents_columns=False)
    lda = models.ldamodel.LdaModel(corpus, num_topics=K_clusters, id2word=id2words)
    print("done in %fs" % (time() - t0))

    output_text = []
    for i, item in enumerate(lda.show_topics(num_topics=K_clusters, num_words=num_display_words, formatted=False)):
        output_text.append("Topic: " + str(i))
        for weight,term in item:
            output_text.append( term + " : " + str(weight) )

    print "writing topics to file:", outputfile
    with open ( outputfile, 'w' ) as f:
        f.write('\n'.join(output_text))


    output_json = []
    for i, item in enumerate(lda.show_topics(num_topics=K_clusters, num_words=num_display_words, formatted=False)):
        topic_terms = {term: str(weight) for weight, term in item}
        output_json.append(topic_terms)

    with open(outputfile + '.json', 'w') as f:
        json.dump(output_json, f)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='This program takes in a file and some parameters and generates topic modeling from the file. This program assumes the file is a line corpus, e.g. list or reviews and outputs the topic with words and weights on the console.')

    parser.add_argument('-f', dest='path2datafile', default="review_sample_100000.txt",
                       help='Specifies the file which is used by to extract the topics. The default file is "review_sample_100000.txt"')

    parser.add_argument('-o', dest='outputfile', default="sample_topics.txt",
                       help='Specifies the output file for the topics, The format is as a topic number followed by a list of words with corresdponding weights of the words. The default output file is "sample_topics.txt"')

    parser.add_argument('-K', default=100, type=int,
                       help='K is the number of topics to use when running the LDA algorithm. Default 100.')
    parser.add_argument('-featureNum', default=50000, type=int,
                       help='feature is the number of features to keep when mapping the bag-of-words to tf-idf vectors, (eg. lenght of vectors). Default featureNum=50000')
    parser.add_argument('-displayWN', default=15,type=int,
                       help='This option specifies how many words to display for each topic. Default is 15 words for each topic.')
    parser.add_argument('--logging', action='store_true',
                       help='This option allows for logging of progress.')


    args = parser.parse_args()
    #print args
    if args.logging:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    print "using input file:", args.path2datafile
    main(args.K, args.featureNum, args.path2datafile, args.displayWN, args.outputfile)

