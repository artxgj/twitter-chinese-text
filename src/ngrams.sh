#!/usr/bin/env bash
tweet_archive_path=~/github/twitter-chinese-text/twitter-2022-06-11-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680/data/tweet.js
csv_prefix_path=~/github/twitter-chinese-text/ngrams

for (( ng=1; ng<=10; ng++ ))
do  
  gen_ngrams="python3 /Users/art/github/twitter-chinese-text/src/hanzi_ngrams_to_csv.py -tweet-js-path ${tweet_archive_path} -csv-prefix-path ${csv_prefix_path} -ngram ${ng}"

  echo ${gen_ngrams}
  ${gen_ngrams}
done
