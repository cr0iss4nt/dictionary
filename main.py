import pymorphy3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from database import get_all_words, analyze_word, clear_db, add_words_from_text, init_db

import tkinter as tk
from tkinter.filedialog import askopenfilename

from file_parser import parse_file


app = Flask(__name__)
init_db()
morph = pymorphy3.MorphAnalyzer()

@app.route('/')
def index():
    words = get_all_words()
    return render_template('index.html', words=words)

@app.route('/clear')
def clear():
    clear_db()
    return redirect(url_for('index'))

@app.route('/analyze/<word_id>')
def add_base_and_ending(word_id):
    analyze_word(word_id)
    return redirect(url_for('index'))

# TODO: do database filling somehow
@app.route('/fill')
def fill():
    root = tk.Tk()

    filename = askopenfilename(filetypes=[("Text files", "*.txt"), ("Rich Text Format documents", "*.rtf")])
    root.withdraw()
    text = parse_file(filename)
    add_words_from_text(text, morph)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)