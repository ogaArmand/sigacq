from django import template

register = template.Library()

@register.filter
def space_separated(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", " ")
    except (ValueError, TypeError):
        return value



@register.filter
def is_pdf(file_url):
    """Vérifie si un fichier est un PDF en se basant sur son extension."""
    return file_url.lower().endswith('.pdf')

# 14156024100002
# 825303V