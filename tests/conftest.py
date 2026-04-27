import pytest
import yaml
from jinja2 import Environment, FileSystemLoader

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIR = os.path.join(BASE_DIR, "core")
DOMAINS_DIR = os.path.join(BASE_DIR, "domains")


def basename_filter(path: str) -> str:
    return os.path.basename(path)


@pytest.fixture
def coding_domain():
    with open(os.path.join(DOMAINS_DIR, "coding.yaml")) as f:
        return yaml.safe_load(f)


@pytest.fixture
def jinja_env():
    env = Environment(loader=FileSystemLoader(CORE_DIR))
    env.filters["basename"] = basename_filter
    return env