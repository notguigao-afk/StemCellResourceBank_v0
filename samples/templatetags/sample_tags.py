from django import template
from django.utils.translation import get_language

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


@register.simple_tag
def localized_date(date_obj):
    """Return a localized date string based on current language"""
    if date_obj is None:
        return ''
    
    lang = get_language() or 'en'
    lang_lower = lang.lower()
    
    # Day of week mappings
    weekdays_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays_zh = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    
    weekday_idx = date_obj.weekday()
    
    if 'zh' in lang_lower:
        # Chinese format: 2024年12月15日 星期一
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year
        weekday = weekdays_zh[weekday_idx]
        return f'{year}年{month}月{day}日 {weekday}'
    else:
        # English format: Monday, December 15, 2024
        weekday = weekdays_en[weekday_idx]
        return date_obj.strftime(f'{weekday}, %B %d, %Y')

