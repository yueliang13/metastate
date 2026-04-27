# Task 003: Create Issue Handling Template

## Project Overview

- **Goal:** Create the generic issue-handling skill template that renders domain-specific issue categories from yaml
- **Architecture:** Jinja2 template parameterized by domain yaml `issues` section
- **Tech Stack:** Python, Jinja2

## Task Objective

Create `core/skills/issue-handling.md.j2` by parameterizing superteam's `skills/hands-off-issue-handling/SKILL.md`. The generic framework (three-state lifecycle, 3-attempt rule, deduplication) stays; domain-specific issue categories, file paths, and ID prefixes come from yaml.

This is Task 3 of 11.

---

**Files:**
- Create: `metastate/core/skills/issue-handling.md.j2`
- Reference: `/Users/yue/Code/Skill/superteam/skills/hands-off-issue-handling/SKILL.md`

- [ ] **Step 1: Create issue-handling.md.j2**

  Read `/Users/yue/Code/Skill/superteam/skills/hands-off-issue-handling/SKILL.md` and parameterize:

  - Keep the generic framework:
    - Three-state lifecycle (Pending → Resolved | Don't Fix)
    - 3+ distinct approaches required before Don't Fix
    - Issues persisted to files, preventing rediscovery
    - Work-object issues must be fixed immediately, not recorded
    - "No issue found" entries and "Notes" sections forbidden
  - Replace hardcoded issue categories with Jinja2 loop:
    ```jinja2
    {% for issue in domain.issues %}
    ## {{ issue.name | title }} Issues

    {% if issue.name == "spec" or issue.name == "brief" %}
    在编写任务文档(task.md)的时候, 需要遵循{{ domain.files.plan_doc | basename }}文档, 如果文档中有模糊不清或前后矛盾的地方, 那么agent就必须自己做出合理假设来解决并记录问题.
    {% endif %}

    路径: {{ issue.file }}
    记录格式:

    ```markdown
    # {{ issue.name | title }} Issues

    ## {{ issue.prefix }}-001: [title]
    - **Description**: [description]
    - **Assumption**: [what we assume to proceed]
    ```
    {% endfor %}
    ```
  - Replace `working/spec-issues.md` etc. with `{{ issue.file }}` template variables
  - Replace `SI-001`, `PI-001`, `EI-001` prefixes with `{{ issue.prefix }}-001`
  - Keep Chinese text in the template (it's from the original and works well for the coding domain)
  - Consider: should the template be in English for broader domains? Add a note about i18n

- [ ] **Step 2: Verify template renders correctly for coding domain**

  Render with coding.yaml issues section and compare against original superteam issue-handling skill. The structure and lifecycle rules must be identical; only the issue category list should differ.