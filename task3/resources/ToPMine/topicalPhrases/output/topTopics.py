f = open('corpus.txt','r')
g = open('topics.txt','r')
h = open('topicalPhrases.txt','w')
phrases = [{} for i in xrange(100)]
for line in f:
    line = line.strip().split(',')
    topics = g.readline().split(',')
    for i in xrange(len(line)):
        topic = topics[i]
        phrase = line[i]
        phrase = phrase.split(" ")
        #greater than 1 means phrase == 1 means unigram
        if len(phrase) > 1:
            phrase = tuple(phrase)
            if phrase in phrases[int(topic)]:
                phrases[int(topic)][phrase]+=1
            else:
                phrases[int(topic)][phrase]=1
for topic in xrange(len(phrases)):
    if len(phrases[topic])>0:
        top = []
        for cand in phrases[topic]:
            top.append((cand, phrases[topic][cand]))
        top.sort(key=lambda x: x[1], reverse=True)
        h = open(str(topic)+'.txt','w')
        for i in xrange(min(50000000,len(top))):
            cand = top[i]
            h.write(" ".join(cand[0])+"\t"+str(cand[1])+"\n")

