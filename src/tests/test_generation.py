import unittest

from src.generator import generate_page


class TestGeneration(unittest.TestCase):

    def test_value_or_children_not_both(self):
        page = generate_page("/content/majesty/index.md", "/template.html", "/public/majesty/index.html")
        page = generate_page("/content/index.md", "/template.html", "/public/index.html")
        pass
