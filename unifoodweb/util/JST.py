import numpy as np
from nltk.corpus import stopwords
import re
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize,sent_tokenize, pos_tag
from nltk.corpus import sentiwordnet as swn
st = PorterStemmer()
from pprint import pprint


MAX_VOCAB_SIZE = 50000


def sampleFromDirichlet(alpha):
    return np.random.dirichlet(alpha)


def sampleFromCategorical(theta):
    theta = theta/np.sum(theta)
    return np.random.multinomial(1, theta).argmax()


def word_indices(wordOccuranceVec):

    wordOccuranceVec = wordOccuranceVec.toarray()[0]
    for idx in wordOccuranceVec.nonzero()[0]:
        for i in range(int(wordOccuranceVec[idx])):
            yield idx


class Jst:

    def __init__(self, numTopics, alpha, beta, gamma, numSentiments=2):

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.numTopics = numTopics
        self.numSentiments = numSentiments

    def processSingleReview(self, review, d=None):
        letters_only = re.sub("[^a-zA-Z]", " ", review)
        words = letters_only.lower().split()
        stops = set(stopwords.words("english"))
        meaningful_words = [st.stem(w) for w in words if w not in stops]
        return(" ".join(meaningful_words))


    def processReviews(self, reviews):
        processed_reviews = []
        i = 0
        for review in reviews:
            if((i + 1) % 1000 == 0):
                print ("Review %d of %d" % (i + 1, len(reviews)))
            processed_reviews.append(self.processSingleReview(review, i))
            i += 1
        self.vectorizer = CountVectorizer(analyzer="word",
                                          tokenizer=None,
                                          preprocessor=None,
                                          stop_words="english",
                                          max_features=MAX_VOCAB_SIZE)
        train_data_features = self.vectorizer.fit_transform(processed_reviews)
        wordOccurenceMatrix = train_data_features
        return wordOccurenceMatrix

    def use_vader(self, sentence):
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(sentence)
        max = 0
        ret = ""
        for k in ss:
            if (k != 'compound'):
                if ss[k] > max:
                    max = ss[k]
                    ret = k
        return ret



    def _initialize_(self, reviews):
        self.wordOccuranceMatrix = self.processReviews(reviews)
        numDocs, vocabSize = self.wordOccuranceMatrix.shape


        # Pseudocounts
        self.n_dt = np.zeros((numDocs, self.numTopics))
        self.n_dts = np.zeros((numDocs, self.numTopics, self.numSentiments))
        self.n_d = np.zeros((numDocs))
        self.n_vts = np.zeros((vocabSize, self.numTopics, self.numSentiments))
        self.n_ts = np.zeros((self.numTopics, self.numSentiments))
        self.topics = {}
        self.sentiments = {}
        self.priorSentiment = {}

        alphaVec = self.alpha * np.ones(self.numTopics)
        gammaVec = self.gamma * np.ones(self.numSentiments)

        for i, word in enumerate(self.vectorizer.get_feature_names()):
            wordSent = self.use_vader(word)
            if(wordSent == 'pos'):
                self.priorSentiment[i] = 1
            if(wordSent == 'neg'):
                self.priorSentiment[i]=0

        for d in range(numDocs):

            topicDistribution = sampleFromDirichlet(alphaVec)
            sentimentDistribution = np.zeros(
                (self.numTopics, self.numSentiments))
            for t in range(self.numTopics):
                sentimentDistribution[t, :] = sampleFromDirichlet(gammaVec)
            for i, w in enumerate(word_indices(self.wordOccuranceMatrix[d, :])):
                t = sampleFromCategorical(topicDistribution)
                s = sampleFromCategorical(sentimentDistribution[t, :])

                self.topics[(d, i)] = t
                self.sentiments[(d, i)] = s
                self.n_dt[d, t] += 1
                self.n_dts[d, t, s] += 1
                self.n_d[d] += 1
                self.n_vts[w, t, s] += 1
                self.n_ts[t, s] += 1



    def conditionalDistribution(self, d, v):

        probabilities_ts = np.ones((self.numTopics, self.numSentiments))
        firstFactor = (self.n_dt[d] + self.alpha) / \
            (self.n_d[d] + self.numTopics * self.alpha)
        secondFactor = (self.n_dts[d, :, :] + self.gamma) / \
            (self.n_dt[d, :] + self.numSentiments * self.gamma)[:, np.newaxis]
        thirdFactor = (self.n_vts[v, :, :] + self.beta) / \
            (self.n_ts + self.n_vts.shape[0] * self.beta)
        probabilities_ts *= firstFactor[:, np.newaxis]
        probabilities_ts *= secondFactor * thirdFactor
        probabilities_ts /= np.sum(probabilities_ts)
        return probabilities_ts

    def getWords(self,indexes):
        vocab = self.vectorizer.get_feature_names()
        return [vocab[i] for i in indexes]



    def getTopKWords(self, K):

        pseudocounts = np.copy(self.n_vts)
        normalizer = np.sum(pseudocounts, (0))
        pseudocounts /= normalizer[np.newaxis, :, :]
        response = []
        for t in range(self.numTopics):
            for s in range(self.numSentiments):
                topWordIndices = pseudocounts[:, t, s].argsort()[-1:-(K + 1):-1]
                vocab = self.vectorizer.get_feature_names()
                response.append((t, s, [vocab[i] for i in topWordIndices]))
        return response


    def run(self, reviews, score, maxIters=30, saveAs=None, saveOverride=False):

        self._initialize_(reviews)
        numDocs, vocabSize = self.wordOccuranceMatrix.shape
        pprint(vocabSize)
        for iteration in range(maxIters):
            print ("Starting iteration %d of %d" % (iteration + 1, maxIters))
            for d in range(numDocs):
                for i, v in enumerate(word_indices(self.wordOccuranceMatrix[d, :])):
                    t = self.topics[(d, i)]
                    s = self.sentiments[(d, i)]
                    self.n_dt[d, t] -= 1
                    self.n_d[d] -= 1
                    self.n_dts[d, t, s] -= 1
                    self.n_vts[v, t, s] -= 1
                    self.n_ts[t, s] -= 1

                    probabilities_ts = self.conditionalDistribution(d, v)
                    if v in self.priorSentiment:
                        s = self.priorSentiment[v]
                        t = sampleFromCategorical(probabilities_ts[:, s])
                    else:
                        if score[d] <= 3:
                            s = 0
                        else:
                            s = 1
                        t = sampleFromCategorical(probabilities_ts[:, s])


                    self.topics[(d, i)] = t
                    self.sentiments[(d, i)] = s
                    self.n_dt[d, t] += 1
                    self.n_d[d] += 1
                    self.n_dts[d, t, s] += 1
                    self.n_vts[v, t, s] += 1
                    self.n_ts[t, s] += 1


