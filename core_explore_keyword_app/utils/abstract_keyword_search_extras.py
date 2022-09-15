""" Abstract Keyword Search Extras
"""
from abc import ABCMeta, abstractmethod


class AbstractKeywordSearchExtras(metaclass=ABCMeta):
    """Abstract Keyword Search Extras"""

    @staticmethod
    @abstractmethod
    def get_extra_html():
        """get_extra_html"""
        raise NotImplementedError("_get_extra_html method is not implemented.")

    @staticmethod
    @abstractmethod
    def get_extra_js():
        """get_extra_js"""
        raise NotImplementedError("_get_extra_js method is not implemented.")

    @staticmethod
    @abstractmethod
    def get_extra_css():
        """get_extra_css"""
        raise NotImplementedError("_get_extra_css method is not implemented.")
