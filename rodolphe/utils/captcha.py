from django.conf import settings

import random
import string

import captcha.fields


class CaptchaField(captcha.fields.CaptchaField):
    def __init__(self, *args, **kwargs):
        if not 'label' in kwargs and hasattr(settings, 'CAPTCHA_LABEL'):
            kwargs['label'] = settings.CAPTCHA_LABEL
        super().__init__(*args, **kwargs)


_DEFAULT_WORDS = [
    string.ascii_uppercase,
    string.digits
]


def find_intruder():
    words_sets = getattr(settings, 'CAPTCHA_WORDS', _DEFAULT_WORDS)
    n_words = getattr(settings, 'CAPTCHA_WORDS_COUNT', 3)

    cat1, cat2 = random.sample(words_sets, 2)
    intruder = random.choice(cat2)
    words = random.sample(cat1, n_words - 1) + [intruder]
    random.shuffle(words)

    return ' '.join(w.upper() for w in words), intruder
