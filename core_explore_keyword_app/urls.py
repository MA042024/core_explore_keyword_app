""" Url router for the explore keyword application
"""

from django.conf.urls import url
from core_explore_keyword_app.views.user import views as user_views

urlpatterns = [
    url(r'^$', user_views.keyword_search,
        name='core_explore_keyword_app_search'),
]
