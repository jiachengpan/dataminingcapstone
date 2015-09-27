java_topic:
	rm -rf CTMindex; java -cp resources/task1JavaTools/textmining.jar topicmodels.CTMMultiRun ./scripts/param.txt

java_mutual:
	java -cp resources/task1JavaTools/textmining.jar functions.MutualInformation categories java_mutual.tsv;./scripts/process_mutual.py


word2vec_train:
	./scripts/word2vec.py train categories/Chinese.txt word2vec.size100.model

word2vec_train_phrase:
	./scripts/word2vec.py train_phrase categories/Chinese.txt word2vec.size100.model 2

word2vec_analyse:
	./scripts/word2vec.py analyse word2vec.size100.model ./external/Chinese.label


segphrase:
	./scripts/run_segphrase.sh
