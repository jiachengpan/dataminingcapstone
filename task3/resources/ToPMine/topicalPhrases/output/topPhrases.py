f = open('corpus.txt','r')
g = open('topPhrases.txt','w')
phrases = {}
for line in f:
    line = line.strip().split(',')
    for phrase in line:
        phrase = phrase.split(" ")
        if len(phrase) > 1:
            phrase = tuple(phrase)
            if phrase in phrases:
                phrases[phrase]+=1
            else:
                phrases[phrase]=1
top = []
for cand in phrases:
    top.append((cand, phrases[cand]))
top.sort(key=lambda x: x[1], reverse=True)
for cand in top:
    g.write(" ".join(cand[0])+"\t"+str(cand[1])+"\n")

