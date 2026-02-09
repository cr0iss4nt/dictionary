from flask import render_template, request

from modules import inflector
from modules.inflector import get_part_of_speech
from __main__ import app, morph


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