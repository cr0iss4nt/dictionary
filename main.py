import os

import pymorphy3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from database import get_all_words, analyze_word, clear_db, add_words_from_text, init_db

from file_parser import parse_file

init_db()
morph = pymorphy3.MorphAnalyzer()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



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


@app.route('/fill', methods=['GET', 'POST'])
def fill():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400

        file = request.files['file']

        if file.filename == '':
            return 'No file selected', 400

        allowed_extensions = ['.txt', '.rtf']
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return 'Invalid file type. Only .txt and .rtf files are allowed.', 400

        try:
            temp_filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(temp_filename)

            text = parse_file(temp_filename)
            add_words_from_text(text, morph)

            if os.path.exists(temp_filename):
                os.remove(temp_filename)

            return redirect(url_for('index'))

        except Exception as e:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            app.logger.error(f'Error processing file: {str(e)}')
            return f'Error processing file: {str(e)}', 500

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)