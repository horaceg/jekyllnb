import os
from collections import namedtuple

import pytest
from pytest_lazyfixture import lazy_fixture

from tests import FILE_NAME


def pytest_configure(config):
    config.addinivalue_line("markers", "unix: mark test to run only on Unix systems")


def parse_file(file):
    lines = file.read().splitlines()
    index = [i for i, x in enumerate(lines) if x == "---"]
    header, body = lines[index[0] + 1 : index[1]], lines[index[1] + 1 :]
    contents = namedtuple("contents", "header body")

    return contents(header, body)


@pytest.fixture(
    autouse=True,
    params=[
        lazy_fixture("app"),
        lazy_fixture("command_line"),
        pytest.param(lazy_fixture("package"), marks=pytest.mark.unix),
    ],
)
def engine():
    pass


@pytest.fixture
def target_contents():
    target_file = os.path.join(
        os.path.dirname(__file__), "resources", FILE_NAME + ".md"
    )

    with open(target_file) as target:
        return parse_file(target)


@pytest.fixture
def test_contents(test_file):
    return parse_file(test_file)