from django import template


register = template.Library()


def addcss(field, css):
    """Add css class to formfield"""
    return field.as_widget(attrs={"class":css})


register.filter('addcss', addcss)
