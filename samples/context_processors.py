from django.utils.translation import get_language
from .models import SiteSettings


def site_settings(request):
    """Context processor to make site settings available in all templates"""
    settings = SiteSettings.get_settings()
    current_language = get_language() or 'en'
    
    # Get site name based on current language (handle both formats)
    lang_lower = current_language.lower()
    if lang_lower in ('zh-hant', 'zh_hant'):
        site_name = settings.site_name_zh_hant
    elif lang_lower in ('zh-hans', 'zh_hans'):
        site_name = settings.site_name_zh_hans
    else:
        site_name = settings.site_name_en
    
    return {
        'site_settings': settings,
        'site_name': site_name,
        'current_language': current_language,
    }

