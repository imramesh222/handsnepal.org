# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='split_at_word')
def split_at_word(value, arg):
    """
    Splits the given text into two parts at the given word count (arg).
    Usage in template:
        {% with value|split_at_word:150 as parts %}
            {{ parts.0 }}   <-- first 150 words
            {{ parts.1 }}   <-- remaining
        {% endwith %}
    """
    try:
        word_limit = int(arg)
        words = value.split()
        part1 = ' '.join(words[:word_limit])
        part2 = ' '.join(words[word_limit:])
        return [part1, part2]
    except Exception:
        return [value, '']
