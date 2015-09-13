process:
	python2 py27_processYelpRestaurants.py --my

lda:
	python2 py27_ldaTopicModeling.py -K 10 -displayWN 100 -f all_reviews.txt

lda_neg:
	python2 py27_ldaTopicModeling.py -K 10 -displayWN 100 -f all_reviews_neg.txt

lda_pos:
	python2 py27_ldaTopicModeling.py -K 10 -displayWN 100 -f all_reviews_pos.txt

auto:
	python2 py27_ldaTopicModeling.py -K 6 -displayWN 100 -f ./categories/Automotive.txt

sea:
	python2 py27_ldaTopicModeling.py -K 6 -displayWN 100 -f ./categories/Seafood_Markets.txt

tour:
	python2 py27_ldaTopicModeling.py -K 6 -displayWN 100 -f ./categories/Tours.txt
