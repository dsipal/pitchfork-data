import sqlite3
from Artist import *
from Review import Review

class Pitchfork(object):
    #db vars
    host = ""
    user = ""
    password = ""
    db = ""

    def __init__(self, artists = {}, reviews = {}):
        self.artists = artists
        self.reviews = reviews
        self._conn = sqlite3.connect('database.sqlite')
        self._c = self._conn.cursor()
        # self._mconn = pymysql.connect(host, user, password, db)
        # self._mc = mconn.cursor()

    def __del__(self):
        self._conn.close()

    def getAllArtists(self):
        self._c.execute("SELECT * FROM artists")
        for row in self._c.fetchall():
            id = row[0]
            name = row[1]
            if name not in self.artists:
                self.artists[name] = Artist(name)

    def getAllReviews(self):
        self._c.execute("SELECT * FROM reviews")
        for row in self._c.fetchall():
            review = Review(row[0],row[1],row[2],row[3],row[4],row[5],row[6])

            if review.artist not in self.artists: self.artists[review.artist] = Artist(review.artist)
            if review.bnm == 1: self.artists[review.artist].bnms.append(review)
            self.artists[review.artist].reviews.append(review)

    def sort(self,type='reviews'):
        if type == 'reviews':
            return(sorted(self.artists.values(), key=lambda artist: len(artist.reviews)))
        if type == 'avg_score':
            return(sorted(self.artists.values(), key=lambda artist: artist.avg_score()))
        else:
            return(sorted(self.artists.values(), key=lambda artist: len(artist.bnms)))

    def getTop(self,count = 50,type='reviews'):
        return(list(self.sort(type))[-count:-1]) ##top one is always "various artists"

    #
    # def syncToServer():
