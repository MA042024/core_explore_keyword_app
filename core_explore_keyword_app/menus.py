""" Add Explore Keyword in main menu
"""

from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

# FIXME: CHECK AUTHENTICATION !
Menu.add_item(
    "main", MenuItem("Query by Keyword", reverse("core_explore_keyword_app_search"))
)
