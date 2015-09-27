#!/bin/bash

inputFile='../rawFiles/Chinese.txt'
# minimum phrase frequency
minsup=10
#maximum size of phrase (number of words)
maxPattern=8
#Two variations of phrase lda (1 and 2). Default topic model is 2
topicModel=2
numTopics=5
#set to 0 for no topic modeling and > 0 for topic modeling (around 1000)
gibbsSamplingIterations=0
#significance threshold for merging unigrams into phrases
thresh=4
#burnin before hyperparameter optimization
optimizationBurnIn=100
#alpha hyperparameter
alpha=2
#optimize hyperparameters every n iterations
optimizationInterval=50
cd TopicalPhrases 
#Run Data preprocessing
./runDataPreparation.sh $inputFile
#Run frequent phrase mining
./runCPM.sh $minsup $maxPattern $thresh
#Run topic modeling
./runPhrLDA.sh $topicModel $numTopics $gibbsSamplingIterations $optimizationBurnIn $alpha $optimizationInterval
#Run post processing (insert stop words and unstem properly)
./createUnStem.sh $inputFile $maxPattern
#Recreate original corpus
python2 unMapper.py input_dataset/input_vocFile input_dataset/input_stemMapping input_dataset_output/unmapped_phrases input_dataset_output/input_partitionedTraining.txt input_dataset_output/newPartition.txt
#Copy to output
cp input_dataset_output/newPartition.txt ../output/corpus.txt
cp input_dataset_output/input_wordTopicAssign.txt ../output/topics.txt
rm input_dataset/*
rm input_dataset_output/*
cd ..
cd output
python2 topPhrases.py
python2 topTopics.py
mv *.txt outputFiles
