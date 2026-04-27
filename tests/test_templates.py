import os

import yaml
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIR = os.path.join(BASE_DIR, "core")
DOMAINS_DIR = os.path.join(BASE_DIR, "domains")


def basename_filter(path: str) -> str:
    return os.path.basename(path)


def get_env():
    env = Environment(loader=FileSystemLoader(CORE_DIR))
    env.filters["basename"] = basename_filter
    return env


def load_coding():
    with open(os.path.join(DOMAINS_DIR, "coding.yaml")) as f:
        return yaml.safe_load(f)


def test_planning_template_renders():
    env = get_env()
    domain = load_coding()
    template = env.get_template("orchestrators/planning.md.j2")
    rendered = template.render(domain=domain)
    assert "Iron Law" in rendered
    assert "planner" in rendered
    assert "plan-reviewer" in rendered
    assert "working/spec.md" in rendered
    assert "digraph" in rendered


def test_executing_template_renders():
    env = get_env()
    domain = load_coding()
    template = env.get_template("orchestrators/executing.md.j2")
    rendered = template.render(domain=domain)
    assert "Iron Law" in rendered
    assert "implementer" in rendered
    assert "EXPECTED" in rendered
    assert "UNEXPECTED" in rendered
    assert "spec-reviewer" in rendered
    assert "code-reviewer" in rendered
    assert "digraph" in rendered


def test_issue_handling_template_renders():
    env = get_env()
    domain = load_coding()
    template = env.get_template("skills/issue-handling.md.j2")
    rendered = template.render(domain=domain)
    assert "SI-001" in rendered
    assert "PI-001" in rendered
    assert "EI-001" in rendered
    assert "working/spec-issues.md" in rendered
    assert "working/plan-issues.md" in rendered
    assert "working/env-issues.md" in rendered
    assert "读取已知问题" in rendered
    assert "记录新问题" in rendered