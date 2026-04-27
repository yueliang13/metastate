# Task 002: Create Core Orchestrator Templates

## Project Overview

- **Goal:** Create the metastate framework — Jinja2 templates that render domain-agnostic state machine orchestrators
- **Architecture:** Jinja2 templates parameterized by domain yaml values
- **Tech Stack:** Python, Jinja2, PyYAML

## Task Objective

Create the two core orchestrator Jinja2 templates (`planning.md.j2` and `executing.md.j2`) by parameterizing superteam's existing `SKILL.md` files. All domain-specific values (agent names, file paths, condition labels) must be replaced with `{{ }}` template variables.

This is Task 2 of 11.

---

**Files:**
- Create: `metastate/core/orchestrators/planning.md.j2`
- Create: `metastate/core/orchestrators/executing.md.j2`
- Reference: `/Users/yue/Code/Skill/superteam/skills/planning/SKILL.md`
- Reference: `/Users/yue/Code/Skill/superteam/skills/executing/SKILL.md`

- [ ] **Step 1: Create planning.md.j2**

  Read `/Users/yue/Code/Skill/superteam/skills/planning/SKILL.md` and parameterize it:
  - Replace `working/spec.md` → `{{ files.plan_doc }}`
  - Replace `working/plan/` → `{{ files.plan_dir }}`
  - Replace `working/plan-review-results.md` → `{{ files.plan_review }}`
  - Replace agent name `planner` → `{{ agents.planner }}`
  - Replace agent names in reviewers → Jinja2 `{% for %}` loop over `agents.plan_reviewers`
  - Replace hardcoded file paths in Agent Prompt Format with template variables
  - Keep Iron Law, verbatim declaration, and NEVER list as-is (domain-agnostic)
  - Add Jinja2 frontmatter for yaml variable access

- [ ] **Step 2: Create executing.md.j2**

  Read `/Users/yue/Code/Skill/superteam/skills/executing/SKILL.md` and parameterize it:
  - Replace `working/plan/` → `{{ files.plan_dir }}`
  - Replace `working/plan/task-NNN/` → `{{ files.task_dir }}` (with `{{ id }}` substitution)
  - Replace all file paths with template variables from yaml
  - Replace `implementer` → `{{ agents.implementer }}`
  - Replace `spec-reviewer`, `code-reviewer` → Jinja2 `{% for %}` loop over `agents.reviewers`
  - Replace `EXPECTED` → `{{ conditions.accept }}`
  - Replace `UNEXPECTED` → `{{ conditions.reject }}`
  - Replace `FIX and SPEC/CODE REVIEW again` → `{{ conditions.rework_label }}`
  - Replace `test-results.md` references → `{{ files.status }}`
  - Replace `changes.md` → `{{ files.output }}`
  - Replace `implement-review-results.md` → `{{ files.review }}`
  - Replace `task.md` → `{{ files.task_doc }}`
  - Replace `commit-message.md` → `{{ files.commit_msg }}`
  - Replace `task-summary.md` → `{{ files.summary }}`
  - Add `disable-model-invocation: true` in frontmatter
  - Keep Iron Law, verbatim declaration, NEVER list as-is
  - Keep agent metrics tracking and output file format sections
  - Parameterize commit message format based on `output.commit_type`

- [ ] **Step 3: Verify templates render correctly**

  Create a test script that renders both templates with the coding domain yaml values and compare output against original superteam files. The rendered output must be functionally equivalent to the originals.

  ```python
  # test_render.py
  from jinja2 import Environment, FileSystemLoader
  import yaml

  with open('domains/coding.yaml') as f:
      domain = yaml.safe_load(f)

  env = Environment(loader=FileSystemLoader('core/orchestrators'))

  for template_name in ['planning.md.j2', 'executing.md.j2']:
      template = env.get_template(template_name)
      rendered = template.render(domain=domain)
      output_path = f'/tmp/test_{template_name.replace(".j2", "")}'
      with open(output_path, 'w') as f:
          f.write(rendered)
      print(f"Rendered {template_name} to {output_path}")
  ```