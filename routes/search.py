from flask import render_template, redirect, url_for, request

from modules.db import get_words
from __main__ import app


@app.route('/search/', methods=['POST'])
def search(query=None):
    query = request.form['query']
    words = get_words(query)
    return render_template('search.html', query=query, words=words)