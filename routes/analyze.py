from flask import redirect, url_for

from modules.db import analyze_word
from __main__ import app


@app.route('/analyze/<word>')
def add_base_and_ending(word):
    analyze_word(word)
    return redirect(url_for('index'))



