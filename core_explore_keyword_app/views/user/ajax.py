"""Explore Example app Ajax views
"""
from core_explore_common_app.views.user.ajax import CreatePersistentQueryUrlView
from core_explore_keyword_app.components.persistent_query_keyword.models import PersistentQueryKeyword


class CreatePersistentQueryUrlKeywordView(CreatePersistentQueryUrlView):
    """ Create the persistent url from a Query
    """

    view_to_reverse = "core_explore_keyword_results_redirect"

    @staticmethod
    def _create_persistent_query(query):
        # create the persistent query
        return PersistentQueryKeyword(user_id=query.user_id,
                                      content=query.content,
                                      templates=query.templates,
                                      data_sources=query.data_sources)
