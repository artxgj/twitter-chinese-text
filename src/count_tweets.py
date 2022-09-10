from twitter_objects import next_tweet, from_tweet_js_file

tweet_js_relparentpaths = (
    '../twitter-2021-12-26-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-01-14-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-01-22-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-02-05-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-04-01-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-05-03-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-05-15-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-05-28-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-06-11-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-06-19-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-07-02-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-07-17-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-08-21-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
    '../twitter-2022-09-10-437b83887b3810705d8f4e1c95fb4abfd78c166a70050b24ff79d6a81806d680',
)

for relpath in tweet_js_relparentpaths:
    tweet_js_filepath = f"./{relpath}/data/tweet.js"
    print(f"{tweet_js_filepath}")
    print(sum(1 for tweet in next_tweet(from_tweet_js_file(tweet_js_filepath))))
    print()

