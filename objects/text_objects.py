# Author Conor O'Kelly

# from vaderSentiment.vaderSentiment import sentiment as VS
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Discription:

    def __init__(self,text,count):

        self.text = text
        self.count = count

class Speech:

    def __init__(self,text,count):

        self.text = text
        self.count = count
        self.sentimnet = self.sentiment_analytis_text()

    def sentiment_analytis_text(self):

        text = self.text

        token_text = tokenize.sent_tokenize(text)
        sid = SentimentIntensityAnalyzer()

        for sentence in token_text:
            print(sentence)
            score = sid.polarity_scores(sentence)
            print(score)

class Scene_change:

    def __init__(self,text,count):

        self.text = text
        self.count = text




if __name__ == '__main__':

    text_ob = Speech("Congratulations, Mike. You deserve it. You're like a totally amazing salesman. You are terribly at your job",0.5)