import os
from abc import abstractmethod
from difflib import Differ
from pprint import pprint
from subprocess import call

import pytest

try:
    from abc import ABC
except ImportError:
    from abc import ABCMeta
    from six import add_metaclass

    @add_metaclass(ABCMeta)
    class ABC:
        pass


FILE_NAME = "hello-world"
SITE_DIR = "docs"
PAGE_DIR = "_pages"
IMAGE_DIR = os.path.join("assets", "images")


class AbstractConfig(ABC):
    @abstractmethod
    @pytest.fixture
    def args(self):
        pass

    @pytest.fixture
    def app(self, args):
        self._app.launch_instance(args)

    @pytest.fixture
    def command(self, args):
        call(["jupyter", self._command] + args)

    @pytest.fixture
    def package(self, args):
        call(["python", "-m", self._command] + args)

    @pytest.fixture(autouse=True)
    def cleanup(self):
        self._app.clear_instance()


class Config(AbstractConfig):  # skipcq: PYL-W0223
    def test_file(self, test_file):  # skipcq: PYL-R0201
        assert test_file.check()

    def test_image(self, image_dir):  # skipcq: PYL-R0201
        assert os.path.isdir(image_dir.strpath)
        assert os.path.isfile(image_dir.join(FILE_NAME + "_4_0.png").strpath)

    def test_header(self, test_contents, target_contents):  # skipcq: PYL-R0201
        try:
            assert all(line in target_contents.header for line in test_contents.header)
        except AssertionError:
            print_diff(test_contents.header, target_contents.header)
            raise

    def test_body(self, test_contents, target_contents):  # skipcq: PYL-R0201
        try:
            assert all(a == b for a, b in zip(test_contents.body, target_contents.body))
        except AssertionError:
            print_diff(test_contents.body, target_contents.body)
            raise


def print_diff(test_lines, target_lines):
    differ = Differ()
    diff = differ.compare(test_lines, target_lines)
    pprint(list(diff))
