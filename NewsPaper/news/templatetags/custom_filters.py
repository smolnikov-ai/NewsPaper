from django import template

register = template.Library()


@register.filter()
def censor(value):
    incorrect_list = ['редиска', 'редиске', 'редиску', 'пидарасами', 'пидарасы', 'пидарасов', 'lgbt']
    correct_value = ''
    new_value = value.replace(',', ' ,').replace('.', ' .').replace(':', ' :').replace(';', ' ;').\
        replace('?', ' ?').replace('!', ' !').replace(')', ' )')
    for word in new_value.split():
        if word.lower() in incorrect_list:
            new_word = word[0] + '*' * (len(word) - 1)
            correct_value += new_word + ' '
        else:
            correct_value += word + ' '
        rezult = correct_value.replace(' ,', ',').replace(' .', '.')\
            .replace(' :', ':').replace(' ;', ';')\
            .replace(' ?', '?').replace(' !', '!').replace(' )', ')')
    return rezult