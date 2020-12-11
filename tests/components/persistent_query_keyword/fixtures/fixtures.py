""" Fixtures files for Persistent Query Keyword
"""
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class PersistentQueryKeywordFixtures(FixtureInterface):
    """Persistent query keyword fixtures"""

    persistent_query_keyword_1 = None
    persistent_query_keyword_2 = None
    persistent_query_keyword_3 = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_query_collection()

    def generate_query_collection(self):
        """Generate a Persistent Query Keyword collection.

        Returns:

        """

        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.persistent_query_keyword_1 = PersistentQueryKeyword(
            user_id="1", name="persistent_query_keyword_1"
        ).save()

        self.persistent_query_keyword_2 = PersistentQueryKeyword(
            user_id="2", name="persistent_query_keyword_2"
        ).save()

        self.persistent_query_keyword_3 = PersistentQueryKeyword(
            user_id="None", name="persistent_query_keyword_3"
        ).save()

        self.data_collection = [
            self.persistent_query_keyword_1,
            self.persistent_query_keyword_2,
            self.persistent_query_keyword_3,
        ]
