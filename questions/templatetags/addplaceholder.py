from django import template


register = template.Library()


def addplaceholder(field, text):
    """Add placeholder to formfield"""
    return field.as_widget(attrs={
        "class": "form-control",
        "placeholder": text,
    })


register.filter('addplaceholder', addplaceholder)
