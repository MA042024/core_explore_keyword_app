from django.conf import settings

if not settings.configured:
    settings.configure()

# MENU
EXPLORE_MENU_NAME = getattr(settings, 'EXPLORE_MENU_NAME', 'Query by Keyword')