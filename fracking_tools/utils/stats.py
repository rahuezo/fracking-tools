from textstat.textstat import textstat as ts
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from files import ExtensionHandler
from files import get_text

import re


class DocumentStats:
    @staticmethod
    def textify(s):
        return ' '.join(re.findall(r'[a-zA-Z]+', s))

    def __init__(self, f, keywords):
        self.f = f
        self.content = ExtensionHandler(self.f).get_content()
        self.keywords = map(lambda x: x.lower(), keywords)

    def get_word_count(self):
        return len(DocumentStats.textify(self.content).split())

    def get_keyword_counts(self):
        content = get_text(self.content).lower()
        counts = {}
        for keyword in self.keywords:
            results = re.findall('{0}'.format(keyword), content)
            if results:
                counts[keyword] = len(results)
            else:
                counts[keyword] = 0
        return counts

    def get_reading_level(self):
        return ts.flesch_kincaid_grade(get_text(self.content))

    def get_sentiment_analysis(self):
        blob = TextBlob(get_text(self.content))
        polarity, subjectivity = blob.sentiment
        blob = TextBlob(get_text(self.content), analyzer=NaiveBayesAnalyzer())
        classification, p_pos, p_neg = blob.sentiment.classification, blob.sentiment.p_pos, blob.sentiment.p_neg
        return [round(polarity, 4), round(subjectivity, 4), classification, round(p_pos, 4), round(p_neg, 4)]

    def compute_all(self):
        reading_level = self.get_reading_level()
        word_count = self.get_word_count()
        keyword_counts_dict = self.get_keyword_counts()
        keyword_counts = [keyword_counts_dict[i] for i in keyword_counts_dict]
        sentiments = self.get_sentiment_analysis()

        # header = ['File', 'Reading Level', 'Word Count'] + [kw.title() for kw in self.keywords] + \
        #          ['Polarity', 'Subjectivity', 'Classification', 'P_POS', 'P_NEG']
        return [reading_level, word_count] + keyword_counts + sentiments


# ds = DocumentStats('content.txt', ['something', 'this', 'document'])
#
# print ds.compute_all()