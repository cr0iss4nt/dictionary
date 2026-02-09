from flask import render_template

from modules.db import get_words
from __main__ import app


@app.route('/')
def index():
    words = get_words()
    return render_template('index.html', words=words)

