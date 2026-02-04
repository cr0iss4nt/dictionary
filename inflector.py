import pymorphy3

def get_part_of_speech(word, morph: pymorphy3.MorphAnalyzer()):
    parsed_word = morph.parse(word)[0]
    return parsed_word.tag.POS

def inflect(word, morph: pymorphy3.MorphAnalyzer(), word_features: set):
    parsed_word = morph.parse(word)[0]
    inflected_word = parsed_word.inflect(word_features)
    return inflected_word[0] if inflected_word is not None else 'Такой формы не существует!'



def inflect_noun(noun, morph: pymorphy3.MorphAnalyzer(), case, number):
    return inflect(noun, morph, {case, number})



def inflect_adjective_singular(adjective, morph: pymorphy3.MorphAnalyzer(), case, gender):
    return inflect(adjective, morph, {case, gender})

def inflect_adjective_plural(adjective, morph: pymorphy3.MorphAnalyzer(), case):
    return inflect(adjective, morph, {case})



def inflect_verb_imperative(verb, morph: pymorphy3.MorphAnalyzer(), number):
    return inflect(verb, morph, {number, 'excl'})

def inflect_verb_past_singular(verb, morph: pymorphy3.MorphAnalyzer(), gender):
    return inflect(verb, morph, {gender, 'sing', 'past'})

def inflect_verb_past_plural(verb, morph: pymorphy3.MorphAnalyzer()):
    return inflect(verb, morph, {'plur', 'past'})

def inflect_verb_present(verb, morph: pymorphy3.MorphAnalyzer(), person, number):
    return inflect(verb, morph, {'pres', person, number})

def inflect_verb_future(verb, morph: pymorphy3.MorphAnalyzer(), person, number):
    return inflect(verb, morph, {'futr', person, number})

