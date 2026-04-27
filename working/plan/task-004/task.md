# Task 004: Create Agent Base Template

## Project Overview

- **Goal:** Create the agent base template with PROMPT GUIDE that helps users write domain-specific agent prompts
- **Architecture:** Jinja2 template with structural skeleton + prompt guide comments
- **Tech Stack:** Python, Jinja2

## Task Objective

Create `core/agents/_base.md.j2` — the structural template for all agent prompts. This template defines the mandatory sections every metastate agent must have (Iron Law, Response Format, Output Files, Process Flow, Issue Handling, NEVER list) with PROMPT GUIDE comments explaining each section.

This is Task 4 of 11.

---

**Files:**
- Create: `metastate/core/agents/_base.md.j2`
- Reference: `/Users/yue/Code/Skill/superteam/agents/implementer.md` (most complete agent example)
- Reference: `/Users/yue/Code/Skill/superteam/agents/planner.md`
- Reference: `/Users/yue/Code/Skill/superteam/agents/spec-reviewer.md`
- Reference: `/Users/yue/Code/Skill/superteam/agents/code-reviewer.md`
- Reference: `/Users/yue/Code/Skill/superteam/agents/plan-reviewer.md`

- [ ] **Step 1: Analyze common patterns across all 5 superteam agents**

  Read all 5 agent files and extract:
  - Common frontmatter fields (name, description, model, skills)
  - Common section structure (Iron Law, Response Format, Output Files, Process Flow, NEVER)
  - Common patterns (issue three-state lifecycle, file-based communication, "NEVER add any extra content")
  - Differences per agent (specific Iron Law text, specific output file format, specific process steps)

- [ ] **Step 2: Create _base.md.j2 with structural skeleton**

  The template must include:
  ```jinja2
  ---
  name: {{ agent_name }}
  description: {{ agent_description }}
  {% if model %}model: {{ model }}{% endif %}
  skills:
  {% for skill in skills %}
    - {{ skill }}
  {% endfor %}
  ---

  # {{ agent_title }} Agent

  {# ============================================================
     PROMPT GUIDE: Fill in your agent's role definition below.

     Every agent in metastate MUST have:
     1. Iron Law — One sentence that constrains the agent's behavior.
        Pattern: "NEVER TRUST THE <role>'s <artifact>."
                 "YOU MUST EXHAUST ALL OPTIONS BEFORE <failure state>."
                 "DO NOT <common mistake for this role>."
     ...
     ============================================================ #}

  ## Iron Law
  {{ iron_law }}

  ## Response Format
  ...

  ## Output Files
  ...

  {# ORCHESTRATOR READS: Mark lines that the orchestrator reads
     for state transitions. These lines MUST NOT change format. #}

  ## Process Flow
  ...

  ## Issue Handling
  ...

  **NEVER:**
  ...
  ```

  Each section must have PROMPT GUIDE comments (in Jinja2 comment blocks so they don't render to output) explaining:
  - Why the section exists
  - What pattern to follow
  - How it connects to the metastate orchestrator
  - Common mistakes to avoid

- [ ] **Step 3: Verify template structure covers all 5 superteam agents**

  For each of the 5 superteam agents, verify that filling in the template would produce a structurally equivalent prompt. The template must be flexible enough to handle:
  - Different numbers of output files (implementer has 2, reviewers share 1)
  - Different Process Flow complexity (implementer has 5 steps, some reviewers have fewer)
  - Different NEVER lists
  - Optional model field (planner and plan-reviewer use opus)