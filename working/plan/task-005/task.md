# Task 005: Create Scaffold Generators

## Project Overview

- **Goal:** Create LLM generation prompts for scaffolding agent prompts and acceptance skills from brief domain descriptions
- **Architecture:** Jinja2 templates that produce LLM prompts (not rendered into dist, but used by `metastate scaffold` command)
- **Tech Stack:** Python, Jinja2

## Task Objective

Create `core/generators/agent.md.j2` and `core/generators/acceptance.md.j2` — LLM generation prompts that take domain yaml + agent descriptions and produce complete agent/acceptance prompts with exemplar-driven quality.

This is Task 5 of 11.

---

**Files:**
- Create: `metastate/core/generators/agent.md.j2`
- Create: `metastate/core/generators/acceptance.md.j2`

- [ ] **Step 1: Create agent.md.j2 generator**

  The generator prompt must produce complete agent prompts that follow the _base.md.j2 structure. It must include:

  1. Role description context from `agent_descriptions`
  2. A complete exemplar agent prompt from the same role type (planner → coding/planner.md, implementer → coding/implementer.md, reviewer → coding/spec-reviewer.md)
  3. The _base.md.j2 structural requirements (Iron Law, Response Format, Output Files, Process Flow, Issue Handling, NEVER list)
  4. Domain context (name, conditions, files, issues)
  5. Instructions to follow the exemplar's structural patterns

  ```jinja2
  You are writing a {{ role_type }} agent prompt for the "{{ domain.name }}" domain in the metastate framework.

  Agent name: {{ agent_name }}
  Agent role: {{ agent_description }}

  This agent is a {{ role_type }} in the metastate workflow:
  {{ role_context }}

  The agent MUST follow these metastate conventions:
  1. Response Format: Output ONLY file paths, no conversational text
  2. Issue Lifecycle: Pending → Resolved | Don't Fix (3+ attempts before Don't Fix)
  3. Read context from files, not from orchestrator
  4. Write results to files per Output Files section

  Here is an example of a high-quality {{ role_type }} agent from the coding domain:

  ---EXAMPLE---
  {{ exemplar_content }}
  ---END EXAMPLE---

  Now generate a complete agent prompt for the "{{ domain.name }}" domain's {{ agent_name }} role.
  Follow the SAME structural patterns as the example:
  - Iron Law: one sentence, inviolable behavioral constraint
  - Response Format: machine-parseable, file paths only
  - Output Files: structured format with ORCHESTRATOR READS markers
  - Process Flow: explicit steps (Read Context → Do Work → Handle Issues → Write Reports)
  - NEVER list: specific anti-patterns for this role
  ```

- [ ] **Step 2: Create acceptance.md.j2 generator**

  The generator prompt must produce acceptance skills that address four mandatory questions:

  ```jinja2
  You are writing an Acceptance Skill for the "{{ domain.name }}" domain in the metastate framework.

  Domain summary: {{ domain.acceptance.summary }}
  Accept condition: {{ domain.acceptance.accept_label }}
  Reject condition: {{ domain.acceptance.reject_label }}

  Your output must follow this structure and address ALL FOUR questions:

  ## What counts as correct output
  [Define domain-specific correctness criteria]

  ## How to verify
  [Define concrete verification methods — commands, tools, procedures]

  ## What is NOT acceptable
  [Define hard rules that MUST NOT be violated]

  ## Verification lifecycle
  [How verification maps to {{ accept_label }}/{{ reject_label }} status]
  [How failures become Pending issues for the next iteration]

  Rules:
  - Be specific and actionable, not vague
  - Every rule must be verifiable
  - Include exact commands or procedures where possible
  - Reference real tools and frameworks appropriate for this domain
  ```

- [ ] **Step 3: Implement self-check logic**

  Create a self-check function that validates generated output has:
  - Iron Law section (for agents)
  - Output Files with ORCHESTRATOR READS markers (for agents)
  - Issue Handling with Pending/Resolved/Don't Fix (for agents)
  - Process Flow with Read Context → Do Work → Handle Issues → Write Reports (for agents)
  - All four mandatory questions addressed (for acceptance skills)

  Missing sections are flagged but don't block generation. The scaffold command should print warnings for missing sections.