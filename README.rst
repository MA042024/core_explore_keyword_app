========================
Core Explore Keyword App
========================

Exploration by keywords for the curator core project.

Quickstart
==========

1. Add "core_explore_keyword_app" to your INSTALLED_APPS setting
----------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        'core_explore_keyword_app',
    ]

Customization
=============

Customize Explore by Keyword search page, by providing additional resources from other applications.

1. Update your custom application to list all the resources that need to be loaded:
-----------------------------------------------------------------------------------

Import AbstractKeywordSearchExtras from core_explore_keyword_app, and implement get_extra_html, get_extra_js,
get_extra_css to provide a list of additional resources.

Example:

.. code:: python

    # Import AbstractKeywordSearchExtras
    from core_explore_keyword_app.utils.abstract_keyword_search_extras import (
        AbstractKeywordSearchExtras,
    )

    # Add a new class that extends AbstractKeywordSearchExtras, and list resources to load
    class CustomKeywordSearchExtras(AbstractKeywordSearchExtras):
        @staticmethod
        def get_extra_html():
            return ["my_custom_app/my_custom_template.html"]

        @staticmethod
        def get_extra_js():
            return [
                {
                    "path": "my_custom_app/js/my_custom_script.js",
                    "is_raw": False,
                },
                {
                    "path": "my_custom_app/js/my_custom_script.raw.js",
                    "is_raw": True,
                }
            ]

        @staticmethod
        def get_extra_css():
            return ["my_custom_app/css/my_custom_stylesheet.css"]



2. Update the project settings to load the resources from your custom application:
----------------------------------------------------------------------------------

.. code:: python

    # Import the CustomKeywordSearchExtras from your package (path and class name may be different)
    from my_custom_app.utils.custom_keyword_search_extras import CustomKeywordSearchExtras
    # Add the class to the EXPLORE_KEYWORD_APP_EXTRAS setting.
    EXPLORE_KEYWORD_APP_EXTRAS = [CustomKeywordSearchExtras]
