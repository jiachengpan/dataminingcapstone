### Coursera Data Mining Capstone Project 

This repository contains all the codes, data and reports that I wrote for this capstone project of [Coursera Data Mining Specialisation](https://class.coursera.org/dataminingcapstone-001).

There are one final report and five reports corresponding to six tasks (the 4th and 5th tasks are combined).

1. [Task I](./task1/report/report.pdf) -- Data Exploration 
  * topic mining among all the yelp reviews for restaurants, and insights from the results
  * topic comparison, and the difference analysis
  * data distribution (rating, review number trend, etc.) of reviews

2. [Task II](./task2/report/report.pdf) -- Cuisine Clustering
  * Cuisine clustering by similarity
  * Clustering result comparison between using different features / results of feature extraction (TF-IDF, LDA)
  * Clustering result comparison between different clustering algorithms (K-means and aglomerative)

3. [Task III](./task3/report/report.pdf) -- Dish Recognition
  * Dish recogntion using three different algorithms, comparison and analysis
    * ToPMine, unsupervised frequent pattern-based phrase mining algorithm
    * SegPhrase, dish mining using external knowledge base, and many other addon features (phrasal segmentation) for quality phrase mining
    * word2vec, dish mining based on word association

4. [Task IV & V](./task4/report/report.pdf) -- Popular Dish and Restaurant Recommendation
  * Rank dishes by ratings, sentiment scores of reviews
  * Restaurant recommendation when given dish name, ranked by similar features
  * Visualisation of the above two results

5. [Task VI](./task6/report.pdf) -- Hygiene Prediction
  * Predict hygiene condition of restaurants based on known features (location, reviews, ratings, tags, etc.)
  * Algorithms used: ensemble algorithms (random forest, xgboost) and regression on top of them

6. [Final Report](./final/report.pdf)
  * A summary of these six tasks
  * Raised some insights of the data set (reviews) that are not mentioned in the earlier tasks
    * what customers may care, which might be helpful to restaurant owners
    * how does the review topic distribute for those 1. frequent yelp users, 2. return customers

