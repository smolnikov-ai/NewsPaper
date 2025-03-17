from django import template

register = template.Library()


@register.filter()
def censor(value):
    incorrect_list = ['Редиск', 'Ананас', 'LGBT']
    for incorrect_word in incorrect_list:
        value = value.replace(incorrect_word[1:], '*' * (len(incorrect_word) - 1))
    return value