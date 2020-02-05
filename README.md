# Discovering spelling variants on Urban Dictionary
Source code of the paper [How to Evaluate Word Representations of Informal Domain?](https://arxiv.org/abs/1911.04669)

## Scraping data from [Urban Dictionary](https://www.urbandictionary.com/)  :bamboo:

* Scraping data from webpage:
```diff
+ scrapy crawl UD
```

* Scrapying data via API:
```diff
+ scrapy crawl UD_API
```
## Bootstrapping algorithms
`UD_Extractor/`

## self-training based CRF tagging
`SeqLabeling/`

## Embedding pretraining with Tweets
train Word2Vec, FastText, GloVe with tweets data. 
`trainEmbedding/'

## Twitter hashtag prediction task using pretrained embedding
Employ Twitter hashtag prediction downstream task using above pretrained informal word vectors as the extrinsic evaluation.
`HashtagPrediction/`

## Analysis
Use Mean Average Precision (MAP) as the intrinsic evaluation rate on word analogy task. Compare the correlations beween the intrinsic and extrinsic tasks.
`calcSim`

## Web interface
informal word pair search tool, written in Flask: `demo/`

