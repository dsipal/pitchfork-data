"""
This script runs the pitchfork_data application using a development server.
"""

from os import environ
from pitchfork_data import app
from Pitchfork import Pitchfork

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
