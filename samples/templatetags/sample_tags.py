from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, key)
    return key


@register.filter
def contains(value, arg):
    """Check if value contains arg (case-insensitive)"""
    if value is None:
        return False
    return arg.lower() in str(value).lower()


@register.simple_tag
def get_language_display(lang_code):
    """Return display name for language code"""
    if lang_code is None:
        return 'English'
    lang_lower = str(lang_code).lower()
    if 'hant' in lang_lower:
        return '繁體中文'
    elif 'hans' in lang_lower:
        return '简体中文'
    return 'English'


@register.simple_tag
def is_language(current_lang, check_lang):
    """Check if current language matches the check language"""
    if current_lang is None:
        current_lang = 'en'
    current_lower = str(current_lang).lower().replace('_', '-')
    check_lower = str(check_lang).lower().replace('_', '-')
    return current_lower == check_lower or check_lower in current_lower

