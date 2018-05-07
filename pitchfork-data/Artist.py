from Review import Review
from operator import itemgetter
class Artist(object):
    def __init__(self, name):
        self.name = name
        self.gender = 'unknown'
        self.reviews = []
        self.bnms = []

    def __str__(self):
        return('Name: ' + self.name)

    def avg_score(self):
        sum = 0
        for review in self.reviews: sum += review.score
        try:
            return(round(sum/len(self.reviews),2))
        except ZeroDivisionError:
            return(0)
    def review_ids(self):
        r = []
        for review in self.reviews:
            r.append(review.id)
        return(r)
    def bnm_ids(self):
        r = []
        for review in self.bnms:
            r.append(review.id)
        return(r)
    def guessGender(self):
        maj = [0,0,0]
        for review in self.reviews:
            pronouns = review.countPronouns()
            for i,b in enumerate(pronouns): maj[i] += b

        if maj[0] > maj[1]: return('feminine')
        if maj[0] < maj[1]: return('masculine')
        else: return('neutral')

    def overallCommonWords(self,count=10,limits=['JJ', 'JJS', 'NN', 'NNP', 'NNS', 'RB', 'RBS', 'UH', 'VB', 'VBG', 'VBP']):
        reviews = []
        most = {}
        for review in self.reviews: reviews.append(review.findCommonWords(limits))

        for review in reviews:
            for word in review:
                if word in reviews:
                    most[word[0]] += word[1]
                else:
                    most[word[0]] = word[1]
        return(sorted(most.items(), key=itemgetter(1))[-count:])
