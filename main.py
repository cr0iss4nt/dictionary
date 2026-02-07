import os
from io import BytesIO

import pymorphy3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file

import inflector
from database import get_all_words, analyze_word, clear_db, add_words_from_text, init_db, db_to_text

from file_parser import parse_file
from inflector import get_part_of_speech

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

@app.route('/analyze/<word>')
def add_base_and_ending(word):
    analyze_word(word)
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

@app.route('/make-word-form/<word>')
def make_word_form(word):
    part_of_speech = get_part_of_speech(word, morph)
    if part_of_speech == 'NOUN':
        return render_template('make_word_form_noun.html', word=word)
    elif part_of_speech == 'ADJF':
        return render_template('make_word_form_adjective.html', word=word)
    elif part_of_speech == 'INFN':
        return render_template('make_word_form_verb.html', word=word)
    else:
        return 'Изменение словоформы для данной части речи недоступно.'

@app.route('/inflect/noun/', methods=['POST'])
def inflect_noun():
    noun = request.form['noun']
    case = request.form['case']
    number = request.form['number']
    inflected_noun = inflector.inflect(noun, morph, {case, number})
    return inflected_noun

@app.route('/inflect/adjective/', methods=['POST'])
def inflect_adjective():
    adjective = request.form['adjective']
    case = request.form['case']
    number = request.form['number']
    gender = request.form['gender']
    inflected_adjective = inflector.inflect(adjective, morph, {case, number, gender})
    return inflected_adjective

@app.route('/inflect/verb/', methods=['POST'])
def inflect_verb():
    verb = request.form['verb']
    mood = request.form['mood']
    number = request.form['number']
    gender = request.form['gender']
    tense = request.form['tense']
    person = request.form['person']
    inflected_verb = inflector.inflect(verb, morph, {mood, number, gender, tense, person})
    return inflected_verb


@app.route('/export')
def export_dictionary():
    try:
        content = db_to_text()

        from datetime import datetime
        filename = f'dictionary_{datetime.today().strftime("%Y%m%d%H%M%S")}.txt'

        file_data = BytesIO(content.encode('utf-8'))

        return send_file(
            file_data,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )

    except Exception as e:
        print(f"Export error: {e}")
        return "Error during export", 500


if __name__ == '__main__':
    app.run(debug=True)