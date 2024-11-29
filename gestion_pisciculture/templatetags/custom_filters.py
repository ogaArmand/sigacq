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


@register.filter
def add_class(field, css):
    """
    Ajoute une classe CSS à un champ de formulaire tout en respectant les attributs existants.
    """
    attrs = field.field.widget.attrs
    existing_classes = attrs.get('class', '')
    updated_classes = f"{existing_classes} {css}".strip()
    attrs['class'] = updated_classes
    return field.as_widget(attrs=attrs)
