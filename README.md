# RhythmRoulette
https://github.com/tobi-1337/RhythmRoulette
## Installation 

# Spotipy

## Installation

Use the package installer (pip) to install Spotipy
'''
pip install Spotipy
'''

## Usage 
'''
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.cache_handler import FlaskSessionCacheHandler
'''

# Config.py
Make a file in this folder called config.py and insert the CLIENT_ID and CLIENT_SECRET from Google Drive(Viktiga länkar)

## Usage
'''
from config import client_id, client_secret, redirect_uri
'''

## Flask
# Installation

Use the package installer (pip) to install Flask

'''
pip install Flask
'''

## Usage
'''
from flask import Flask, render_template, url_for, session, redirect, request
'''