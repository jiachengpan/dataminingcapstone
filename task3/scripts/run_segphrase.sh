#! /bin/bash


cd ./resources/SegPhrase/
./train.exp.sh
cd -

awk -F',' '
  NF == 2 {
    gsub(/_/, " ", $1);
    print $1;
  }
  NF == 1 {
    print tolower($0)
  }
' ./external/Chinese ./resources/SegPhrase/results/salient.csv > tmp.segphrase

awk -F'\t' '{if ($2 == 1) print $1}' ./resources/SegPhrase/results/autolabel > tmp.autolabel

cat tmp.autolabel tmp.segphrase |head -n 10000 | sed '1i Chinese' > segphrase.result
