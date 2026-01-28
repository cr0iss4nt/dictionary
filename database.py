import sqlite3
import pymorphy3

from lexemizer import text_to_lexemes

DATABASE_NAME = 'dictionary.db'

def init_db():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dictionary (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL,
    part_of_speech TEXT NOT NULL,
    base TEXT NOT NULL,
    ending TEXT NOT NULL,
    bases_on INTEGER DEFAULT NULL
    )
    ''')

    connection.commit()
    connection.close()

def get_all_words():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Dictionary WHERE bases_on = NULL")
    words = cursor.fetchall()

    connection.close()

    return words

def add_base_word(word, part_of_speech):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO Dictionary(word, part_of_speech, base, ending, bases_on)
    VALUES
    (?, ?, '', '', NULL)
    ''', (word, part_of_speech))

    connection.commit()
    connection.close()

def add_words_from_text(text, morph: pymorphy3.MorphAnalyzer()):
    lexemes = text_to_lexemes(text, morph)
    for lexeme in lexemes:
        part_of_speech = morph.parse(lexeme)[0].tag.POS
        add_base_word(lexeme, part_of_speech)