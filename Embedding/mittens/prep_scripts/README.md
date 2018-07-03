Before experimenting, preprocess wikipedia with:
```
python prep_scripts/wikipedia_process.py $CORPUSDIR/wikipedia/ > $CORPUSDIR/wikipedia_en.txt
./vocab_count -min-count 100 < $CORPUSDIR/wikipedia_en.txt > $CORPUSDIR/wikipedia_en.txt.vocab
~/mittens/prep_scripts/count.sh $CORPUSDIR/wikipedia_en.txt
```

And Twitter with:
```
python prep_scripts/twitter_process.py --rootdir /ambrosia/nyx/disk3/processedTweets --verbose > $CORPUSDIR/twitter_en.txt
./vocab_count -min-count 100 < $CORPUSDIR/twitter_en.txt > $CORPUSDIR/twitter_en.txt.vocab.tmp
perl -lne 'print unless /^(@|http)/' $CORPUSDIR/twitter_en.txt.vocab.tmp > $CORPUSDIR/twitter_en.txt.vocab
~/mittens/prep_scripts/count.sh $CORPUSDIR/twitter_en.txt
```

Then run:
```
python ./old_vocab_to_new.py $CORPUSDIR/wikipedia_en.txt.vocab $CORPUSDIR/twitter_en.txt.vocab > $CORPUSDIR/wiki2twittervocab.txt
```
