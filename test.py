
import os
dirpath='/disk/data/wmagdy/TweetCrawlers/General/data'

for datafile in os.listdir(dirpath):
    path = os.path.join(dirpath, datafile)
    with open(path,'r', encoding='utf8') as f:
        for line in f.readlines():
            print(line)
            pass