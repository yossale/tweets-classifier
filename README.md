# tweets-classifier

to run:
pip install nltk

python tweets-classifier.py <LabeledTrainingData.tsv> <RealData.tsv> <ResFile.tsv>

###LabeledTrainingData 
Should be in this **tsv** format:
```TweetId TweetContent  Label```
i.e:
```
398065503257624576	@sandsra_ I wanna unfollow that btch. HAHAHA. If you know... :)	good
281190412952141825	Search intensifies for NYC shooter; video released -	bad
```

###RealData
Should be in this **tsv** format:
```TweetId TweetContent```
i.e: 
```
470168824571256832	@Vosskah @Rhidach so much hate for the awesome Paladin
470168328397680640	@ItsaMiri a lot of my coworkers play in Tampa/St Pete area, but I also have an iPhone /grrrr
```

###ResFile
is in this **tsv** format:
```TweetId TweetContent  Guess```
i.e:
```
398065503257624576	@sandsra_ I wanna unfollow that btch. HAHAHA. If you know... :)	good
281190412952141825	Search intensifies for NYC shooter; video released -	bad
```


