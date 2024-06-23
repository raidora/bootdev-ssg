import os
import unittest

from src.file_manager import find_root_dir_r
from src.generator import generate_page, generate_pages_recursive


class TestGeneration(unittest.TestCase):

    def test_gen_page(self):
        page = generate_page("/content/majesty/index.md", "/template.html", "/public/majesty/index.html")
        page = generate_page("/content/index.md", "/template.html", "/public/index.html")
        pass

    def test_gen_page_r(self):
        root_dir = find_root_dir_r(os.path.dirname(os.path.realpath(__file__)))
        generate_pages_recursive(root_dir+"/content", root_dir+"/template.html", root_dir+"/public")
        pass
