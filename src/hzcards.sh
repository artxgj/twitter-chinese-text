#!/usr/bin/env bash

rm  /Users/arthurkho/github/twitter-chinese-text/nippon_2/*.md
echo
ls /Users/arthurkho/github/twitter-chinese-text/nippon_2/*.md
echo

python3 ./hanzi_study_cards.py  -cards-study-path /Users/arthurkho/github/twitter-chinese-text/nippon_2 -summary-csv-path /Users/arthurkho/github/twitter-chinese-text/inputs/summary_tweets_chinese_text.csv -tweets-vocab-index-path /Users/arthurkho/github/twitter-chinese-text/indexes/tweets_vocab_index.dat -vocab-tweets-index-path /Users/arthurkho/github/twitter-chinese-text/indexes/vocab_tweets_index.dat

echo
echo "honeycomb"
