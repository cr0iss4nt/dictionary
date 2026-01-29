import sqlite3
import pymorphy3

from lexemizer import text_to_lexemes
from word_analyzer import make_session, get_base_and_ending

DATABASE_NAME = 'dictionary.db'

def init_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dictionary (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL UNIQUE,
    part_of_speech TEXT NOT NULL,
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
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Dictionary")
    words = cursor.fetchall()

    connection.close()

    return words

def add_base_word(word, part_of_speech, base, ending):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO Dictionary(word, part_of_speech, base, ending)
    VALUES
    (?, ?, ?, ?)
    ''', (word, part_of_speech, base, ending))

    connection.commit()
    connection.close()

def add_words_from_text(text, morph: pymorphy3.MorphAnalyzer()):
    lexemes = text_to_lexemes(text, morph)
    for lexeme in lexemes:
        part_of_speech = morph.parse(lexeme)[0].tag.POS
        add_base_word(lexeme, part_of_speech, '', '')
        print("Added word:", lexeme)

def analyze_word(word_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT word FROM Dictionary where id=?
    ''',(word_id,))
    word = cursor.fetchone()[0]

    base, ending = get_base_and_ending(word)

    cursor.execute('''
    UPDATE Dictionary
    SET base=?, ending=?
    WHERE id=?
    ''', (base, ending, word_id))

    connection.commit()
    connection.close()