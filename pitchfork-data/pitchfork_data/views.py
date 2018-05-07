"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from pitchfork_data import app
from Pitchfork import Pitchfork

db = Pitchfork()
db.getAllArtists()
db.getAllReviews()

@app.route('/')
def index():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/search', methods=['GET'])
def search():
    query = request.values.get('q')
    results = []

    for key, item in db.artists.items(): 
        if query in key: results.append(item)

    return render_template('results.html', query=query, results=results)

@app.route('/artist/<artist>')
def artist(artist):
    artist = db.artists[artist]
    

    return render_template(
        'artist.html',
        title=artist,
        name = artist.name,
        avg_score = artist.avg_score(),
        gender_guess = artist.guessGender(),
        adjectives = artist.overallCommonWords(5,['JJ','JJS','JJR']),
        verbs = artist.overallCommonWords(5,['VB', 'VBG', 'VBP']),
        reviews = artist.reviews,
        year=datetime.now().year
    )
