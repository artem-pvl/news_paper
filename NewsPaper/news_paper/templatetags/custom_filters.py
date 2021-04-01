from django import template

register = template.Library()


BAD_DICT = [
    'хуй',
    'хуе',
    'хуё',
    'пизд',
    'ебат',
    'ебан',
    'ебал',
    'бля',
]


@register.filter(name='censor')
def censor(text: str):
    text_list = text.split()
    for i in range(len(text_list)):
        for bad in BAD_DICT:
            if text_list[i].lower().find(bad) >= 0:
                text_list[i] = '-пик-'
    return ' '.join(text_list)
