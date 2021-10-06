"""  Menu configuration for core_main_app. Upon installation of the app the following
menus are displayed:

  * User menu

    * `core_explore_keyword_app.settings.EXPLORE_MENU_NAME`

  * Admin menu

    * Explore by keyword
        * Search operators
"""
from django.urls import reverse
from menu import Menu, MenuItem

from core_explore_keyword_app.settings import EXPLORE_MENU_NAME

# FIXME: CHECK AUTHENTICATION !
Menu.add_item(
    "main", MenuItem(EXPLORE_MENU_NAME, reverse("core_explore_keyword_app_search"))
)

explore_by_keyword_children = (
    MenuItem(
        "Search Operators",
        reverse("core-admin:core_explore_keyword_app_list_search_operators"),
        icon="code",
    ),
)

Menu.add_item(
    "admin", MenuItem("EXPLORE BY KEYWORD", None, children=explore_by_keyword_children)
)
