# Task 006: Implement metastate build Command

## Project Overview

- **Goal:** Implement the `metastate build --domain <name>` CLI command that renders all templates and produces a complete Claude Code plugin
- **Architecture:** Python CLI with Jinja2 rendering and file copying
- **Tech Stack:** Python, Jinja2, PyYAML

## Task Objective

Implement the `metastate build` command in `metastate.py` that reads a domain yaml, renders all Jinja2 templates, copies domain-specific files, and produces a complete Claude Code plugin in `dist/<domain>/`.

This is Task 6 of 11.

---

**Files:**
- Modify: `metastate/metastate.py`
- Reference: Design spec "Build Process" section

- [ ] **Step 1: Implement domain yaml loading and validation**

  ```python
  import yaml

  def load_domain(domain_name: str) -> dict:
      """Load and validate domain yaml."""
      path = f"domains/{domain_name}.yaml"
      with open(path) as f:
          domain = yaml.safe_load(f)

      # Validate required fields
      required = ['name', 'description', 'agents', 'conditions', 'files', 'issues']
      for field in required:
          if field not in domain:
              raise ValueError(f"Missing required field '{field}' in {path}")

      # Validate agents
      agents = domain['agents']
      if 'planner' not in agents or 'implementer' not in agents:
          raise ValueError("Domain must have planner and implementer agents")

      # Validate conditions
      conds = domain['conditions']
      for field in ['accept', 'reject', 'rework_label']:
          if field not in conds:
              raise ValueError(f"Missing condition '{field}'")

      return domain
  ```

- [ ] **Step 2: Implement Jinja2 template rendering**

  ```python
  from jinja2 import Environment, FileSystemLoader

  def render_templates(domain: dict, output_dir: str):
      """Render all core templates with domain config."""
      env = Environment(loader=FileSystemLoader('core'))
      domain_data = {'domain': domain}

      # Render orchestrators
      for orchestrator in domain.get('orchestrators', ['planning', 'executing']):
          template = env.get_template(f'orchestrators/{orchestrator}.md.j2')
          rendered = template.render(**domain_data)
          skill_dir = f"{output_dir}/skills/{orchestrator}"
          os.makedirs(skill_dir, exist_ok=True)
          with open(f"{skill_dir}/SKILL.md", 'w') as f:
              f.write(rendered)

      # Render issue-handling skill
      template = env.get_template('skills/issue-handling.md.j2')
      rendered = template.render(**domain_data)
      skill_dir = f"{output_dir}/skills/issue-handling"
      os.makedirs(skill_dir, exist_ok=True)
      with open(f"{skill_dir}/SKILL.md", 'w') as f:
              f.write(rendered)
  ```

- [ ] **Step 3: Implement file copying**

  ```python
  import shutil

  def copy_domain_files(domain: dict, domain_name: str, output_dir: str):
      """Copy domain-specific agents and skills to output."""
      domain_dir = f"domains/{domain_name}"

      # Copy agents
      agents_dir = f"{domain_dir}/agents"
      if os.path.exists(agents_dir):
          dest = f"{output_dir}/agents"
          os.makedirs(dest, exist_ok=True)
          for f in os.listdir(agents_dir):
              if f.endswith('.md'):
                  shutil.copy2(f"{agents_dir}/{f}", f"{dest}/{f}")

      # Copy domain skills
      for skill_name in domain.get('domain_skills', []):
          src = f"{domain_dir}/skills/{skill_name}.md"
          if os.path.exists(src):
              dest = f"{output_dir}/skills/{skill_name}"
              os.makedirs(dest, exist_ok=True)
              shutil.copy2(src, f"{dest}/SKILL.md")
  ```

- [ ] **Step 4: Implement plugin.json generation**

  ```python
  import json

  def generate_plugin_json(domain: dict, output_dir: str):
      """Generate .claude_plugin/plugin.json from domain config."""
      plugin_dir = f"{output_dir}/.claude_plugin"
      os.makedirs(plugin_dir, exist_ok=True)
      plugin = {
          "name": domain['name'],
          "description": domain['description'],
          "version": "1.0.0"
      }
      with open(f"{plugin_dir}/plugin.json", 'w') as f:
          json.dump(plugin, f, indent=2)
  ```

- [ ] **Step 5: Implement validation step**

  After building, validate that:
  - All agents referenced in domain yaml exist as files
  - All file paths referenced in templates are consistent
  - Required skills directory structure exists

  ```python
  def validate_build(domain: dict, domain_name: str, output_dir: str):
      """Validate built plugin has all referenced agents."""
      agents = domain['agents']
      all_agent_names = [agents['planner'], agents['implementer']] + \
                        agents.get('plan_reviewers', []) + \
                        agents.get('reviewers', [])
      for agent_name in all_agent_names:
          agent_file = f"{output_dir}/agents/{agent_name}.md"
          if not os.path.exists(agent_file):
              print(f"WARNING: Agent file not found: {agent_file}")
  ```

- [ ] **Step 6: Wire up cmd_build in metastate.py**

  ```python
  def cmd_build(args):
      """Build a Claude Code plugin from domain config."""
      domain_name = args.domain
      domain = load_domain(domain_name)
      output_dir = f"dist/{domain_name}"

      # Clean output
      if os.path.exists(output_dir):
          shutil.rmtree(output_dir)

      render_templates(domain, output_dir)
      copy_domain_files(domain, domain_name, output_dir)
      generate_plugin_json(domain, output_dir)
      validate_build(domain, domain_name, output_dir)

      print(f"Built {domain_name} plugin to {output_dir}")
  ```

- [ ] **Step 7: Test with coding domain**

  Create `domains/coding.yaml` (from design spec) and run:
  ```bash
  python metastate.py build --domain coding
  ```
  Verify `dist/coding/` has correct structure with rendered templates.