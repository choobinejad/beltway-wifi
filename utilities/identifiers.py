import string
import random
import nltk
from nltk.corpus import gutenberg, stopwords
from nltk import word_tokenize


# TODO this touches the interwebs
nltk.download('gutenberg')
nltk.download('stopwords')
nltk.download('punkt')
stop = stopwords.words('english') + list(string.punctuation)
stop += [str(i) for i in range(500)]
# Some things to exclude from the randomness. They can make awkward combinations.
stop += ['husband']
raw = gutenberg.words('melville-moby_dick.txt')
words = list(set([i.lower() for i in word_tokenize(' '.join(raw)) if i.lower() not in stop and len(i) > 4]))[:400]


def generate_mac_address(oui=None, ordinal=None):

    # Configure Options
    if oui:
        target_length = 6
    else:
        target_length = 12

    if ordinal:
        choices = int(ordinal)
    else:
        choices = random.randint(0, 16 ** target_length)

    # Make the MAC
    big_hex = hex(choices)[2:].zfill(target_length)

    # Format output
    if oui:
        formatted = '{}:{}{}:{}{}:{}{}'.format(oui, *big_hex)
    else:
        formatted = '{}{}:{}{}:{}{}:{}{}:{}{}:{}{}'.format(*big_hex)

    return formatted


def generate_words(n=2):
    name = ''
    for i in range(n):
        name += '-' + random.choice(words)
    return name[1:]
