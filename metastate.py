#!/usr/bin/env python3
"""Metastate CLI — domain-agnostic state machine framework."""
import argparse
import json
import os
import shutil
import sys

import yaml
from jinja2 import Environment, FileSystemLoader


def basename_filter(path: str) -> str:
    """Jinja2 filter: return the basename of a path."""
    return os.path.basename(path)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(BASE_DIR, "core")
DOMAINS_DIR = os.path.join(BASE_DIR, "domains")


def load_domain(domain_name: str) -> dict:
    """Load and validate domain yaml."""
    path = os.path.join(DOMAINS_DIR, f"{domain_name}.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Domain config not found: {path}")
    with open(path) as f:
        domain = yaml.safe_load(f)

    required = ["name", "description", "agents", "conditions", "files", "issues"]
    for field in required:
        if field not in domain:
            raise ValueError(f"Missing required field '{field}' in {path}")

    agents = domain["agents"]
    if "planner" not in agents or "implementer" not in agents:
        raise ValueError("Domain must have planner and implementer agents")

    conds = domain["conditions"]
    for field in ["accept", "reject", "rework_label"]:
        if field not in conds:
            raise ValueError(f"Missing condition '{field}'")

    return domain


def render_templates(domain: dict, output_dir: str):
    """Render all core templates with domain config."""
    env = Environment(loader=FileSystemLoader(CORE_DIR))
    env.filters["basename"] = basename_filter
    domain_data = {"domain": domain}

    orchestrators = domain.get("orchestrators", ["planning", "executing"])
    for orchestrator in orchestrators:
        template = env.get_template(f"orchestrators/{orchestrator}.md.j2")
        rendered = template.render(**domain_data)
        skill_dir = os.path.join(output_dir, "skills", orchestrator)
        os.makedirs(skill_dir, exist_ok=True)
        with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
            f.write(rendered)

    template = env.get_template("skills/issue-handling.md.j2")
    rendered = template.render(**domain_data)
    skill_dir = os.path.join(output_dir, "skills", "issue-handling")
    os.makedirs(skill_dir, exist_ok=True)
    with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
        f.write(rendered)


def copy_domain_files(domain: dict, domain_name: str, output_dir: str):
    """Copy domain-specific agents and skills to output."""
    domain_dir = os.path.join(DOMAINS_DIR, domain_name)
    skill_mappings = domain.get("skill_mappings", {})

    agents_dir = os.path.join(domain_dir, "agents")
    if os.path.exists(agents_dir):
        dest = os.path.join(output_dir, "agents")
        os.makedirs(dest, exist_ok=True)
        for fname in os.listdir(agents_dir):
            if fname.endswith(".md"):
                src_path = os.path.join(agents_dir, fname)
                dest_path = os.path.join(dest, fname)
                with open(src_path) as f:
                    content = f.read()
                for old, new in skill_mappings.items():
                    content = content.replace(old, new)
                with open(dest_path, "w") as f:
                    f.write(content)

    for skill_name in domain.get("domain_skills", []):
        src_dir = os.path.join(domain_dir, "skills")
        # Support both single-file (skill_name.md) and directory (skill_name/SKILL.md) layouts
        src_file = os.path.join(src_dir, f"{skill_name}.md")
        src_skill_dir = os.path.join(src_dir, skill_name)
        if os.path.exists(src_file):
            dest = os.path.join(output_dir, "skills", skill_name)
            os.makedirs(dest, exist_ok=True)
            shutil.copy2(src_file, os.path.join(dest, "SKILL.md"))
        elif os.path.isdir(src_skill_dir):
            dest = os.path.join(output_dir, "skills", skill_name)
            shutil.copytree(src_skill_dir, dest, dirs_exist_ok=True)


def generate_plugin_json(domain: dict, output_dir: str):
    """Generate .claude_plugin/plugin.json from domain config."""
    plugin_dir = os.path.join(output_dir, ".claude_plugin")
    os.makedirs(plugin_dir, exist_ok=True)
    plugin = {
        "name": domain["name"],
        "description": domain["description"],
        "version": "1.0.0",
    }
    with open(os.path.join(plugin_dir, "plugin.json"), "w") as f:
        json.dump(plugin, f, indent=2)


def validate_build(domain: dict, domain_name: str, output_dir: str):
    """Validate built plugin has all referenced agents."""
    agents = domain["agents"]
    all_agent_names = [agents["planner"], agents["implementer"]] + \
                      agents.get("plan_reviewers", []) + \
                      agents.get("reviewers", [])
    for agent_name in all_agent_names:
        agent_file = os.path.join(output_dir, "agents", f"{agent_name}.md")
        if not os.path.exists(agent_file):
            print(f"WARNING: Agent file not found: {agent_file}")


ROLE_EXEMPLARS = {
    "planner": "coding/planner.md",
    "implementer": "coding/implementer.md",
    "reviewer": "coding/spec-reviewer.md",
}


def determine_role_type(agent_name: str) -> str:
    """Determine role type from agent name."""
    name_lower = agent_name.lower()
    if "planner" in name_lower or "plan" in name_lower:
        return "planner"
    if "reviewer" in name_lower or "review" in name_lower or "checker" in name_lower:
        return "reviewer"
    if "implement" in name_lower:
        return "implementer"
    return "implementer"


def get_role_context(role_type: str) -> str:
    """Get context description for a role type."""
    contexts = {
        "planner": "Creates plans from input documents. Plans must be executable by agents with zero context. Bite-sized tasks with verification steps.",
        "implementer": "Implements a single task and fixes issues. Exhausts all options before Don't Fix. Follows TDD or domain-appropriate methodology.",
        "reviewer": "Reviews work output for correctness and quality. Never trusts claims, verifies everything independently. Creates review result files.",
    }
    return contexts.get(role_type, contexts["implementer"])


def get_exemplar(role_type: str) -> str | None:
    """Find best exemplar agent from existing domains."""
    exemplar_path = ROLE_EXEMPLARS.get(role_type)
    full_path = os.path.join(DOMAINS_DIR, exemplar_path) if exemplar_path else None
    if full_path and os.path.exists(full_path):
        with open(full_path) as f:
            return f.read()
    return None


def generate_agent_prompt(domain: dict, agent_name: str, agent_description: str) -> str:
    """Generate agent prompt from description + exemplar."""
    env = Environment(loader=FileSystemLoader(CORE_DIR))
    template = env.get_template("generators/agent.md.j2")

    exemplar = get_exemplar(determine_role_type(agent_name))

    return template.render(
        domain=domain,
        agent_name=agent_name,
        agent_description=agent_description,
        exemplar_content=exemplar or "No exemplar available",
        role_type=determine_role_type(agent_name),
        role_context=get_role_context(determine_role_type(agent_name)),
    )


def generate_acceptance_skill(domain: dict) -> str:
    """Generate acceptance skill from domain summary."""
    env = Environment(loader=FileSystemLoader(CORE_DIR))
    template = env.get_template("generators/acceptance.md.j2")
    return template.render(domain=domain)


def check_agent_prompt(content: str) -> list[str]:
    """Check generated agent prompt has all required sections."""
    warnings = []
    if "## Iron Law" not in content:
        warnings.append("Missing Iron Law section")
    if "## Response Format" not in content:
        warnings.append("Missing Response Format section")
    if "## Output Files" not in content:
        warnings.append("Missing Output Files section")
    if "## Process Flow" not in content and "## Process" not in content:
        warnings.append("Missing Process Flow section")
    if "ORCHESTRATOR READS" not in content:
        warnings.append("Missing ORCHESTRATOR READS markers in Output Files")
    return warnings


def check_acceptance_skill(content: str) -> list[str]:
    """Check acceptance skill addresses all four mandatory questions."""
    warnings = []
    required_sections = [
        "What counts as correct output",
        "How to verify",
        "What is NOT acceptable",
        "Verification lifecycle",
    ]
    for section in required_sections:
        if section.lower() not in content.lower():
            warnings.append(f"Missing section: {section}")
    return warnings


def cmd_build(args):
    """Build a Claude Code plugin from domain config."""
    domain_name = args.domain
    domain = load_domain(domain_name)
    output_dir = os.path.join(BASE_DIR, "dist", domain_name)

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    render_templates(domain, output_dir)
    copy_domain_files(domain, domain_name, output_dir)
    generate_plugin_json(domain, output_dir)
    validate_build(domain, domain_name, output_dir)

    print(f"Built {domain_name} plugin to {output_dir}")


def cmd_scaffold(args):
    """Scaffold domain files from descriptions."""
    domain_name = args.domain
    domain = load_domain(domain_name)

    output_dir = os.path.join(DOMAINS_DIR, domain_name)
    os.makedirs(os.path.join(output_dir, "agents"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "skills"), exist_ok=True)

    agents_config = domain["agents"]
    all_agents = {"planner": agents_config["planner"],
                  "implementer": agents_config["implementer"]}
    for reviewer in agents_config.get("plan_reviewers", []):
        all_agents[reviewer] = reviewer
    for reviewer in agents_config.get("reviewers", []):
        all_agents[reviewer] = reviewer

    for agent_name, desc in agents_config.get("agent_descriptions", {}).items():
        prompt = generate_agent_prompt(domain, agent_name, desc)
        warnings = check_agent_prompt(prompt)
        agent_file = os.path.join(output_dir, "agents", f"{agent_name}.md")
        with open(agent_file, "w") as f:
            f.write(prompt)
        print(f"Generated {agent_file}")
        for w in warnings:
            print(f"  WARNING: {w}")

    acceptance = generate_acceptance_skill(domain)
    warnings = check_acceptance_skill(acceptance)
    acceptance_file = os.path.join(output_dir, "skills", "acceptance.md")
    with open(acceptance_file, "w") as f:
        f.write(acceptance)
    print(f"Generated {acceptance_file}")
    for w in warnings:
        print(f"  WARNING: {w}")


def main():
    parser = argparse.ArgumentParser(description="Metastate CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build plugin from domain")
    build_parser.add_argument("--domain", required=True, help="Domain name")
    build_parser.set_defaults(func=cmd_build)

    scaffold_parser = subparsers.add_parser("scaffold", help="Scaffold domain files")
    scaffold_parser.add_argument("--domain", required=True, help="Domain name")
    scaffold_parser.set_defaults(func=cmd_scaffold)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()