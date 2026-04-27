# Task 008: Migrate Coding Domain from Superteam

## Project Overview

- **Goal:** Extract superteam's coding-specific content into metastate's coding domain, creating the first complete domain that validates the framework
- **Architecture:** Copy agent prompts, adapt black-box-testing skill into acceptance skill, create coding.yaml
- **Tech Stack:** Python, Jinja2

## Task Objective

Create the coding domain by extracting content from `/Users/yue/Code/Skill/superteam/` and adapting it for metastate's structure. This is the validation domain — if `metastate build --domain coding` produces output functionally equivalent to superteam, the framework works.

This is Task 8 of 11.

---

**Files:**
- Create: `metastate/domains/coding.yaml`
- Create: `metastate/domains/coding/agents/planner.md`
- Create: `metastate/domains/coding/agents/implementer.md`
- Create: `metastate/domains/coding/agents/spec-reviewer.md`
- Create: `metastate/domains/coding/agents/code-reviewer.md`
- Create: `metastate/domains/coding/agents/plan-reviewer.md`
- Create: `metastate/domains/coding/skills/acceptance.md`
- Reference: `/Users/yue/Code/Skill/superteam/agents/*.md`
- Reference: `/Users/yue/Code/Skill/superteam/skills/black-box-testing/SKILL.md`

- [ ] **Step 1: Create coding.yaml**

  Use the coding domain example from the design spec. Verify all fields match superteam's hardcoded values.

- [ ] **Step 2: Copy agent prompts from superteam**

  Copy each agent file, making these adaptations:
  - Keep Iron Law, Process Flow, Output Files, NEVER list as-is
  - Keep domain-specific content (TDD, code organization, testing) as-is
  - The agents remain domain-specific content — they are NOT parameterized

  ```bash
  cp /Users/yue/Code/Skill/superteam/agents/planner.md metastate/domains/coding/agents/
  cp /Users/yue/Code/Skill/superteam/agents/implementer.md metastate/domains/coding/agents/
  cp /Users/yue/Code/Skill/superteam/agents/spec-reviewer.md metastate/domains/coding/agents/
  cp /Users/yue/Code/Skill/superteam/agents/code-reviewer.md metastate/domains/coding/agents/
  cp /Users/yue/Code/Skill/superteam/agents/plan-reviewer.md metastate/domains/coding/agents/
  ```

- [ ] **Step 3: Adapt black-box-testing skill into acceptance.md**

  Read `/Users/yue/Code/Skill/superteam/skills/black-box-testing/SKILL.md` and adapt it:
  - Keep the black-box testing rules and TDD methodology
  - Keep the Chinese text (it works well for the coding domain)
  - Change frontmatter name from `black-box-testing` to `acceptance`
  - The content remains coding-specific — this is the domain's acceptance skill

- [ ] **Step 4: Verify build produces equivalent output**

  Run `metastate build --domain coding` and compare `dist/coding/` against superteam's structure:
  - `dist/coding/skills/planning/SKILL.md` ≈ superteam's `skills/planning/SKILL.md` (parameterized version)
  - `dist/coding/skills/executing/SKILL.md` ≈ superteam's `skills/executing/SKILL.md` (parameterized version)
  - `dist/coding/skills/issue-handling/SKILL.md` ≈ superteam's `skills/hands-off-issue-handling/SKILL.md` (parameterized version)
  - `dist/coding/skills/acceptance/SKILL.md` ≈ superteam's `skills/black-box-testing/SKILL.md` (adapted)
  - `dist/coding/agents/*.md` = superteam's `agents/*.md` (identical copies)