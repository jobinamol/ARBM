from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiply the arg by the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return '' 