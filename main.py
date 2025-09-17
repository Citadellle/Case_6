# Part of case-study #6
# Case has been done by Mihail Gordeev, Sergey Chirkov and Nezhinsky Dmitriy

from textblob import TextBlob
from mtranslate import translate
from re import sub
import ru_local as ru


def sentiment_analysis(x):
    '''function get polarity index and return mood in string type.
    The polarity score is a float within the range [-1.0, 1.0]'''
    text = TextBlob(x)
    pol = text.sentiment.polarity

    #return frase instead if index
    if pol > 0.1:
        return ru.POSITIVE
    elif pol < -0.1:
        return ru.NEGATIVE
    else:
        return ru.NEUTRAL


def text_objectivity(x):
    '''function geting objectivity index.
    The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective'''
    text = TextBlob(x)
    obv = text.sentiment.subjectivity

    return f'{(100 - obv*100).__round__(2)}%'


def translate_rus_to_eng(text):
    '''function translates the incoming text from Russian to English'''
    translated_text = translate(text, 'en', 'auto')

    return translated_text


def number_syllables_per_word(word):
    '''function counts the number of syllables in a word
    number of vowels is same to the number of syllables in a word'''
    vowels = ['a', 'e', 'i', 'o', 'u',
              'а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я']
    syllables = 0
    for vowel in vowels:
        syllables += word.lower().count(vowel)

    return syllables


def number_syllables_per_text(text):
    '''function counts the number of syllables in the text'''
    syllables = 0
    text_without_punctuation_marks = sub(r'[^\w\s]', '', text)

    for word in text_without_punctuation_marks.split():
        syllables += number_syllables_per_word(word)

    return syllables


def average_number_of_syllables_per_word(text):
    '''function counts the average number of syllables per word'''
    asw = number_syllables_per_text(text) / count_words(text)

    return asw


def count_sentences(text):
    '''function counts the number of sentences in the text
    function count all the end-of-sentence signs'''
    dots = text.count('.')
    exclamations = text.count('!')
    questions = text.count('?')
    ellipses = text.count('...')

    return dots + exclamations + questions + ellipses


def count_words(text):
    '''function counts the number of words in the text
    function count all the spaces in the text'''
    if not text:
        return 0

    text_without_punctuation_marks = sub(r'[^\w\s]', '', text)
    spaces = text_without_punctuation_marks.count(' ')

    return spaces + 1


def average_sentence_length(text):
    '''function calculates the average length of a sentence in the text
    average number of words in a sentence'''
    sentences = count_sentences(text)
    words = count_words(text)

    if sentences == 0:
        return 0

    return words / sentences


def FRE(x):
    '''this function count Flash index with use other additional function'''
    return 206.835 - 1.015 * (count_words(x) / count_sentences(x)) - 84.6 * (number_syllables_per_text(x) / count_words(x))


def FRE_options(x):
    '''function ranks FRE index and return string data about readability'''
    if FRE(x) > 80:
        return ru.EASY_READING
    elif FRE(x) > 50:
        return ru.SIMPLE_READING
    elif FRE(x) > 25:
        return ru.HARD_READING
    return ru.SO_HARD_READING


def main():
    '''main function that outputs the necessary information'''
    text = input('Введите текст: ')

    print(f'{ru.SENTENCES} {count_sentences(text)}\n')

    print(f'{ru.WORDS} {count_words(text)}\n')

    print(f'{ru.SYLLABLES} {number_syllables_per_text(text)}\n')

    print(f'{ru.MIDLLE_WORD} {average_sentence_length(text)}\n')

    print(f'{ru.MIDLLE_SYL} {average_number_of_syllables_per_word(text)}\n')

    print(f'{ru.FRE} {FRE(text)}\n\n'
          f'{FRE_options(text)}\n')

    print(f'{ru.SENTIMENT} {sentiment_analysis(text)}\n')

    print(f'{ru.OBJECTIVE} {text_objectivity(text)}')


if __name__ == '__main__':

    main()

