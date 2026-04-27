# Task 011: Scaffold and Validate Copywriting Domain + README

## Project Overview

- **Goal:** Complete the copywriting domain validation and write project documentation
- **Architecture:** Same as Task 010 for copywriting, plus README documentation
- **Tech Stack:** Python, Jinja2

## Task Objective

Scaffold the copywriting domain, build it, verify it's distinct from coding, and write the project README that explains how to use metastate.

This is Task 11 of 11.

---

**Files:**
- Create: `metastate/domains/copywriting.yaml` (from design spec)
- Generate: `metastate/domains/copywriting/agents/*.md`
- Generate: `metastate/domains/copywriting/skills/acceptance.md`
- Create: `metastate/README.md`

- [ ] **Step 1: Create copywriting.yaml**

  Use the copywriting domain example from the design spec.

- [ ] **Step 2: Run scaffold and review output**

  ```bash
  python metastate.py scaffold --domain copywriting
  ```

  Review generated files for:
  - Brand voice compliance checking in reviewers
  - Editorial review methodology
  - APPROVED/REJECTED conditions
  - No coding-specific terminology

- [ ] **Step 3: Refine generated output**

  Same refinement process as Task 010 Step 3.

- [ ] **Step 4: Build copywriting domain**

  ```bash
  python metastate.py build --domain copywriting
  ```

  Verify `dist/copywriting/` has correct structure with APPROVED/REJECTED conditions, writer/editor/brand-reviewer agents, and BI/SI/EI issue prefixes.

- [ ] **Step 5: Write README.md**

  ```markdown
  # Metastate

  Domain-agnostic state machine framework for AI-driven workflows.

  ## Quick Start

  ```bash
  # Build an existing domain
  python metastate.py build --domain coding
  claude --plugin-dir dist/coding

  # Scaffold a new domain
  # 1. Create domains/mydomain.yaml
  # 2. Run scaffold
  python metastate.py scaffold --domain mydomain
  # 3. Review and refine generated files in domains/mydomain/
  # 4. Build
  python metastate.py build --domain mydomain
  claude --plugin-dir dist/mydomain
  ```

  ## How It Works

  Metastate separates the workflow skeleton (state machine topology, issue lifecycle, file conventions) from the domain meat (agent prompts, acceptance criteria, file formats).

  - **Skeleton** is defined in Jinja2 templates under `core/`
  - **Meat** is defined in domain yaml configs and agent prompts under `domains/`
  - **Build** renders templates + copies domain files → complete Claude Code plugin
  - **Scaffold** generates agent prompts and acceptance skills from brief descriptions

  ## Adding a New Domain

  1. Create `domains/mydomain.yaml` with agents, conditions, files, issues
  2. Run `python metastate.py scaffold --domain mydomain`
  3. Review and refine generated files
  4. Run `python metastate.py build --domain mydomain`
  5. Use `claude --plugin-dir dist/mydomain`

  ## Included Domains

  - **coding** — Software development with TDD (migrated from superteam)
  - **research** — Research and analysis with fact-checking
  - **copywriting** — Brand copywriting with editorial review
  ```

- [ ] **Step 6: Final validation — all three domains build successfully**

  ```bash
  python metastate.py build --domain coding
  python metastate.py build --domain research
  python metastate.py build --domain copywriting
  ```

  Verify each `dist/<domain>/` has:
  - `.claude_plugin/plugin.json`
  - `skills/planning/SKILL.md`
  - `skills/executing/SKILL.md`
  - `skills/issue-handling/SKILL.md`
  - `skills/acceptance/SKILL.md`
  - `agents/<all referenced agents>.md`

  Each domain must use its own condition labels (EXPECTED/VERIFIED/APPROVED), agent names, and file paths.