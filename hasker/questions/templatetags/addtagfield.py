from django import template


register = template.Library()


def addtagfield(field, placeholder):
    """Add placeholder to formfield"""
    return field.as_widget(attrs={
        "class": "form-control",
        "placeholder": placeholder,
        "data-role": "tagsinput",
    })


register.filter('addtagfield', addtagfield)
