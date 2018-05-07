import sqlite3
import re
import nltk
from nltk import tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from operator import itemgetter


class Review(object):
    
    def __init__(self,  id = 0, album = '', artist = '', url = '', score = 0.0, bnm = 0, author = '', date = ''):
        self.id = id
        self.artist = artist
        self.album = album
        self.url = url
        self.score = score
        self.bnm = bnm
        self.author = author
        self.date = date

    def __str__(self):
        return(self.artist + " - " + self.album + ": " + str(self.score))

    def word_count(self):
        return(len(word_tokenize(self.getContent())))

    def getContent(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute("SELECT content FROM content WHERE reviewid = {}".format(self.id))

        return(''.join(c.fetchone()))

    def countPronouns(self):
        content = self.getContent()
        FEMININEPRONOUNS = ['her','Her','she','She']
        MASCULINEPRONOUNS = ['his', 'His','he','He']
        NEUTRALPRONOUNS = ['their', 'Their', 'they', 'They']
        count = [0,0,0] # fem,masc,neut

        for word in word_tokenize(re.sub('\W+', " ", content)[:-1]):
            if word in FEMININEPRONOUNS: count[0] += 1
            if word in MASCULINEPRONOUNS: count[1] += 1
            if word in NEUTRALPRONOUNS: count[2] += 1

        return(count)

    def findCommonWords(self, limits = ['JJ', 'JJS', 'NN', 'NNP', 'NNS', 'RB', 'RBS', 'UH', 'VB', 'VBG', 'VBP']):
        common = {}
        for word in nltk.pos_tag(word_tokenize(re.sub('\W+', " ", self.getContent()))):
            if word[1] in limits and len(word[0]) > 1:
                if word[0] not in common:
                    common[word[0]] = 1
                else:
                    common[word[0]] += 1
        return(sorted(common.items(), key=itemgetter(1)))
