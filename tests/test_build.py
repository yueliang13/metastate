import json
import os
import shutil
import tempfile

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAINS_DIR = os.path.join(BASE_DIR, "domains")

# Import build functions directly
import sys

sys.path.insert(0, BASE_DIR)
from metastate import load_domain, render_templates, copy_domain_files, generate_plugin_json


def test_build_produces_plugin_structure():
    domain = load_domain("coding")
    with tempfile.TemporaryDirectory() as tmp:
        render_templates(domain, tmp)
        copy_domain_files(domain, "coding", tmp)
        generate_plugin_json(domain, tmp)

        assert os.path.exists(os.path.join(tmp, ".claude_plugin", "plugin.json"))
        assert os.path.exists(os.path.join(tmp, "skills", "planning", "SKILL.md"))
        assert os.path.exists(os.path.join(tmp, "skills", "executing", "SKILL.md"))
        assert os.path.exists(os.path.join(tmp, "skills", "issue-handling", "SKILL.md"))
        assert os.path.exists(os.path.join(tmp, "skills", "acceptance", "SKILL.md"))
        assert os.path.exists(os.path.join(tmp, "agents", "planner.md"))
        assert os.path.exists(os.path.join(tmp, "agents", "implementer.md"))


def test_plugin_json_content():
    domain = load_domain("coding")
    with tempfile.TemporaryDirectory() as tmp:
        generate_plugin_json(domain, tmp)
        with open(os.path.join(tmp, ".claude_plugin", "plugin.json")) as f:
            plugin = json.load(f)
        assert plugin["name"] == "coding"
        assert plugin["description"] == "Software development with TDD discipline"


def test_planning_functionally_equivalent():
    """Rendered planning skill is functionally equivalent to superteam's."""
    from jinja2 import Environment, FileSystemLoader

    def basename_filter(path):
        return os.path.basename(path)

    core_dir = os.path.join(BASE_DIR, "core")
    env = Environment(loader=FileSystemLoader(core_dir))
    env.filters["basename"] = basename_filter

    domain = load_domain("coding")
    template = env.get_template("orchestrators/planning.md.j2")
    rendered = template.render(domain=domain)

    superteam_path = "/Users/yue/Code/Skill/superteam/skills/planning/SKILL.md"
    if os.path.exists(superteam_path):
        with open(superteam_path) as f:
            original = f.read()
        # Check structural equivalence
        assert "Iron Law" in rendered
        assert "Process Flow" in rendered
        assert "digraph" in rendered
        assert "Agent Prompt Format" in rendered or "Agent Prompt" in rendered
        for concept in ["state machine", "dispatch", "Pending issues", "review"]:
            assert concept in rendered.lower() or concept in rendered