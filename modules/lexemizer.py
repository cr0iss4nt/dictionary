from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy3

RUSSIAN_LETTERS = 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДДЖЭЯЧСМИТЬБЮЁйцукенгшщзхъфывапролджэячсмитьбюё'

def is_russian_text(text):
    return not set(text) - set(RUSSIAN_LETTERS)

def tokenize_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('russian'))
    filtered_tokens = [word for word in tokens if word not in stop_words and is_russian_text(word)]
    return filtered_tokens

def tokens_to_lexemes(tokens, morph: pymorphy3.MorphAnalyzer()):
    lexemes = set()
    for token in tokens:
        p = morph.parse(token)[0]
        lexemes.add(p.normal_form)
    return sorted(list(lexemes))

def text_to_lexemes(text, morph: pymorphy3.MorphAnalyzer()):
    tokens = tokenize_text(text)
    lexemes = tokens_to_lexemes(tokens, morph)
    return lexemes

