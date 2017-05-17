"""Core Explore Keyword App views
"""
from core_main_app.utils.rendering import render


def index(request):
    """ Explore by keyword index view

    Args:
        request:

    Returns:

    """
    assets = {}
    context = {}

    return render(request,
                  'core_explore_keyword_app/user/index.html',
                  assets=assets,
                  context=context)
