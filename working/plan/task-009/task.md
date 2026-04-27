# Task 009: Validate Build Output Against Superteam

## Project Overview

- **Goal:** Verify that `metastate build --domain coding` produces output functionally equivalent to superteam
- **Architecture:** Comparison testing between rendered templates and original superteam files
- **Tech Stack:** Python, pytest

## Task Objective

Write tests that verify the rendered coding domain plugin matches superteam's original files in structure and content. This validates the entire template system works correctly.

This is Task 9 of 11.

---

**Files:**
- Create: `metastate/tests/test_build.py`
- Create: `metastate/tests/test_templates.py`
- Create: `metastate/tests/conftest.py`

- [ ] **Step 1: Create test infrastructure**

  ```python
  # conftest.py
  import pytest
  import yaml
  from jinja2 import Environment, FileSystemLoader

  @pytest.fixture
  def coding_domain():
      with open('domains/coding.yaml') as f:
          return yaml.safe_load(f)

  @pytest.fixture
  def jinja_env():
      return Environment(loader=FileSystemLoader('core'))
  ```

- [ ] **Step 2: Write template rendering tests**

  ```python
  # test_templates.py
  def test_planning_template_renders(jinja_env, coding_domain):
      """Planning template renders without errors for coding domain."""
      template = jinja_env.get_template('orchestrators/planning.md.j2')
      rendered = template.render(domain=coding_domain)
      assert 'Iron Law' in rendered
      assert 'dispatch planner' in rendered
      assert 'plan-reviewer' in rendered
      assert 'working/spec.md' in rendered

  def test_executing_template_renders(jinja_env, coding_domain):
      """Executing template renders without errors for coding domain."""
      template = jinja_env.get_template('orchestrators/executing.md.j2')
      rendered = template.render(domain=coding_domain)
      assert 'Iron Law' in rendered
      assert 'dispatch implementer' in rendered
      assert 'EXPECTED' in rendered
      assert 'UNEXPECTED' in rendered
      assert 'spec-reviewer' in rendered
      assert 'code-reviewer' in rendered

  def test_issue_handling_template_renders(jinja_env, coding_domain):
      """Issue handling template renders with correct issue categories."""
      template = jinja_env.get_template('skills/issue-handling.md.j2')
      rendered = template.render(domain=coding_domain)
      assert 'SI-001' in rendered
      assert 'PI-001' in rendered
      assert 'EI-001' in rendered
  ```

- [ ] **Step 3: Write build output tests**

  ```python
  # test_build.py
  def test_build_produces_plugin_structure(tmp_path, coding_domain):
      """Build produces correct plugin directory structure."""
      # Run build
      build_domain(coding_domain, 'coding', str(tmp_path))
      # Check directory structure
      assert (tmp_path / '.claude_plugin' / 'plugin.json').exists()
      assert (tmp_path / 'skills' / 'planning' / 'SKILL.md').exists()
      assert (tmp_path / 'skills' / 'executing' / 'SKILL.md').exists()
      assert (tmp_path / 'skills' / 'issue-handling' / 'SKILL.md').exists()
      assert (tmp_path / 'skills' / 'acceptance' / 'SKILL.md').exists()
      assert (tmp_path / 'agents' / 'planner.md').exists()
      assert (tmp_path / 'agents' / 'implementer.md').exists()

  def test_plugin_json_content(tmp_path, coding_domain):
      """Plugin.json has correct name and description."""
      build_domain(coding_domain, 'coding', str(tmp_path))
      with open(tmp_path / '.claude_plugin' / 'plugin.json') as f:
          plugin = json.load(f)
      assert plugin['name'] == 'coding'
      assert plugin['description'] == 'Software development with TDD discipline'
  ```

- [ ] **Step 4: Write functional equivalence test**

  ```python
  def test_planning_equivalent_to_superteam(jinja_env, coding_domain):
      """Rendered planning skill is functionally equivalent to superteam's."""
      template = jinja_env.get_template('orchestrators/planning.md.j2')
      rendered = template.render(domain=coding_domain)

      # Read original superteam planning skill
      with open('/Users/yue/Code/Skill/superteam/skills/planning/SKILL.md') as f:
          original = f.read()

      # Check structural equivalence
      assert 'Iron Law' in rendered
      assert 'Process Flow' in rendered
      assert 'digraph' in rendered
      assert 'Agent Prompt Format' in rendered

      # Check all key concepts are present
      for concept in ['state machine', 'dispatch', 'Pending issues', 'review']:
          assert concept in rendered
  ```

- [ ] **Step 5: Run all tests and verify passing**

  ```bash
  cd /Users/yue/Code/Skill/metastate && python -m pytest tests/ -v
  ```