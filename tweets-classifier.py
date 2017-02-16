import nltk
import random
import re
import csv
import sys

STOP_WORDS = [
    "a",
"about",
"above",
"after",
"again",
"against",
"all",
"am",
"an",
"and",
"any",
"are",
"aren't",
"as",
"at",
"be",
"because",
"been",
"before",
"being",
"below",
"between",
"both",
"but",
"by",
"can't",
"cannot",
"could",
"couldn't",
"did",
"didn't",
"do",
"does",
"doesn't",
"doing",
"don't",
"down",
"during",
"each",
"few",
"for",
"from",
"further",
"had",
"hadn't",
"has",
"hasn't",
"have",
"haven't",
"having",
"he",
"he'd",
"he'll",
"he's",
"her",
"here",
"here's",
"hers",
"herself",
"him",
"himself",
"his",
"how",
"how's",
"i",
"i'd",
"i'll",
"i'm",
"i've",
"if",
"in",
"into",
"is",
"isn't",
"it",
"it's",
"its",
"itself",
"let's",
"me",
"more",
"most",
"mustn't",
"my",
"myself",
"no",
"nor",
"not",
"of",
"off",
"on",
"once",
"only",
"or",
"other",
"ought",
"our",
"ours",
"ourselves",
"out",
"over",
"own",
"same",
"shan't",
"she",
"she'd",
"she'll",
"she's",
"should",
"shouldn't",
"so",
"some",
"such",
"than",
"that",
"that's",
"the",
"their",
"theirs",
"them",
"themselves",
"then",
"there",
"there's",
"these",
"they",
"they'd",
"they'll",
"they're",
"they've",
"this",
"those",
"through",
"to",
"too",
"under",
"until",
"up",
"very",
"was",
"wasn't",
"we",
"we'd",
"we'll",
"we're",
"we've",
"were",
"weren't",
"what",
"what's",
"when",
"when's",
"where",
"where's",
"which",
"while",
"who",
"who's",
"whom",
"why",
"why's",
"with",
"won't",
"would",
"wouldn't",
"you",
"you'd",
"you'll",
"you're",
"you've",
"your",
"yours",
"yourself",
"yourselves"]

http_re = re.compile(r'\s+http://[^\s]*')
remove_ellipsis_re = re.compile(r'\.\.\.')
at_sign_re = re.compile(r'\@\S+')
hash_sign_re = re.compile(r'\#\S+')
punct_re = re.compile(r"[\"'\[\],.:;()\-&!]")
price_re = re.compile(r"\d+\.\d\d")
stop_words_re = re.compile('|'.join(STOP_WORDS).lower())

# converts to lower case and clean up the text
def normalize_tweet(tweet):
    t = tweet.lower()

    t = re.sub(price_re, 'PRICE', t)
    t = re.sub(remove_ellipsis_re, '', t)
    t = re.sub(http_re, ' LINK', t)
    t = re.sub(punct_re, '', t)
    # t = re.sub(at_sign_re, 'TAG', t)
    # t = re.sub(hash_sign_re, 'HASH', t)
    return t

def tweet_features(tweet_data):
    features = {}

    normalized_tweet = normalize_tweet(tweet_data['content'])
    # print 'tweet: [%s] -> normalized: [%s]' % (tweet_data['content'], normalized_tweet)
    for trigram in nltk.trigrams(normalized_tweet.split(' ')):
        features['contains(%s)' % ','.join(trigram)] = True

    return features

data = []
posSamples = 0
negSamples = 0

for line in open(sys.argv[1]):
    csv_row = line.strip().split('\t')
    if len(csv_row) != 3:
        print 'Failed to parse: [%s]' % (line)
    else:
        dataPoint = { 'id': csv_row[0], 'content': csv_row[1], 'label': csv_row[2] }
        data.append(dataPoint)
        if (csv_row[2] == 'bad'):
            negSamples = negSamples + 1
        else:
            posSamples = posSamples + 1

# we split the data into two parts
# the first part (90% of the data) is for training
# the remaining 10% of the data is for testing
size = int(len(data) * 0.8)

train_data = data[:size]
test_data = data[size:]

# generate features for tweet
train_set = [ (tweet_features(d), d['label']) for d in train_data ]
test_set  = [ (tweet_features(d), d['label']) for d in test_data  ]

# pick a classifier
classifier = nltk.NaiveBayesClassifier


# train classifier using training set
classifier = nltk.NaiveBayesClassifier.train(train_set)




# collect tweets that were wrongly classified
errors = []
fp = 0
fn = 0
tp = 0
tn = 0

for d in test_data:
    label = d['label']
    guess = classifier.classify(tweet_features(d))
    if guess != label:
        errors.append( (label, guess, d) )
        if guess == 'good': 
            fp = fp + 1 
        else: 
            fn = fn + 1
    else:
        if guess == 'bad':
            tn = tn + 1
        else:
            tp = tp + 1

for (label, guess, d) in sorted(errors):
    print 'correct label: %s\nguessed label: %s\ntweet=%s\n' % (label, guess, d['content'])

print 'Total errors: %d' % len(errors)
print 'fp: [%s]. fn: [%s], tp: [%s], tn: [%s]' % (fp,fn,tp,tn)
print 'Total test size: %s. Pos: [%s], Neg: [%s] precision: [%s], recall: [%s]' % (len(test_data), posSamples, negSamples, 1.0 * tp / (tp + fp), 1.0 * tp / (tp + fn) )

print 'Accuracy: ', nltk.classify.accuracy(classifier, test_set)

classifier.show_most_informative_features(20)

processedLines = 0
with open(sys.argv[3], "w") as resFile:
    for line in open(sys.argv[2]):
        csv_row = line.strip().split('\t')
        if len(csv_row) != 2:
            print 'Failed to parse: [%s]' % (line)
        else:
            processedLines = processedLines + 1
            dataPoint = { 'id': csv_row[0], 'content': csv_row[1] }
            guess = classifier.classify(tweet_features(dataPoint))
            label = '0' if guess == 'bad' else '1'
            resFile.write("\t".join([dataPoint['id'], label]) + "\n")
            
print 'Labeled %s lines, Results are at %s' % (processedLines, sys.argv[3])