import sqlite3

import pymorphy3

from lexemizer import text_to_lexemes
from word_analyzer import get_base_and_ending

DATABASE_NAME = 'dictionary.db'

def init_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dictionary (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL UNIQUE,
    part_of_speech TEXT,
    base TEXT NOT NULL,
    ending TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def clear_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Dictionary")

    connection.commit()
    connection.close()

def get_all_words():
    init_db()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Dictionary ORDER BY word")
    words = cursor.fetchall()

    connection.close()

    return words

def add_normalized_word(word, part_of_speech, base, ending):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute('''
        INSERT INTO Dictionary(word, part_of_speech, base, ending)
        VALUES
        (?, ?, ?, ?)
        ''', (word, part_of_speech, base, ending))
        print(f"Added word: {word}")
    except:
        print(f"Error adding word: {word}")

    connection.commit()
    connection.close()

def add_words_from_text(text, morph: pymorphy3.MorphAnalyzer()):
    lexemes = text_to_lexemes(text, morph)
    for lexeme in lexemes:
        add_word(lexeme, morph)

def add_word(word, morph: pymorphy3.MorphAnalyzer()):
    part_of_speech = morph.parse(word)[0].tag.POS
    add_normalized_word(word, part_of_speech, '', '')

# change the base and the ending of the word
def edit_word(word, base, ending):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    UPDATE Dictionary
    SET base=?, ending=?
    WHERE word=?
    ''', (base, ending, word))

    connection.commit()
    connection.close()

def analyze_word(word):
    base, ending = get_base_and_ending(word)

    edit_word(word, base, ending)

def delete_word(word):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    DELETE FROM Dictionary
    WHERE word=?
    ''', (word,))

    connection.commit()
    connection.close()

def db_to_text():
    words = get_all_words()
    output = []
    for word in words:
        output.append(f"""{word[1].upper()}
Часть речи: {word[2]}
Основа: {word[3]}
Окончание: {word[4]}""")
    return '\n\n\n'.join(output)