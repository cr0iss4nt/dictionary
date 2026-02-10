from flask import render_template, redirect, url_for

from modules.db import get_words
from __main__ import app


@app.route('/search/')
@app.route('/search/<query>')
def search(query=None):
    if query is None:
        return redirect(url_for('index'))

    words = get_words(query)
    return render_template('search.html', query=query, words=words)