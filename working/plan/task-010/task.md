# Task 010: Scaffold and Validate Research Domain

## Project Overview

- **Goal:** Use `metastate scaffold --domain research` to generate the research domain and validate the framework works for a new domain
- **Architecture:** LLM-generated agent prompts + acceptance skill from domain descriptions
- **Tech Stack:** Python, Jinja2

## Task Objective

Create the research domain yaml, run scaffold to generate agent prompts and acceptance skill, review and refine the output, then build and verify the research domain plugin.

This is Task 10 of 11.

---

**Files:**
- Create: `metastate/domains/research.yaml` (from design spec)
- Generate: `metastate/domains/research/agents/*.md`
- Generate: `metastate/domains/research/skills/acceptance.md`
- Validate: `metastate/dist/research/` build output

- [ ] **Step 1: Create research.yaml**

  Use the research domain example from the design spec. Verify all fields are consistent and complete.

- [ ] **Step 2: Run scaffold and review output**

  ```bash
  python metastate.py scaffold --domain research
  ```

  Review each generated file:
  - `domains/research/agents/research-planner.md` — Does it have Iron Law, Process Flow, Output Files?
  - `domains/research/agents/researcher.md` — Does it have verification steps, source hierarchy?
  - `domains/research/agents/fact-checker.md` — Does it have independent verification behavior?
  - `domains/research/agents/methodology-reviewer.md` — Does it review methodology quality?
  - `domains/research/skills/acceptance.md` — Does it address all four mandatory questions?

- [ ] **Step 3: Refine generated output**

  For each generated file:
  - Fix any structural issues flagged by self-check
  - Ensure ORCHESTRATOR READS markers are present in Output Files
  - Ensure Issue Handling section references correct file paths from research.yaml
  - Ensure Process Flow follows Read Context → Do Work → Handle Issues → Write Reports pattern
  - Ensure Iron Law is one sentence and domain-appropriate

- [ ] **Step 4: Build research domain**

  ```bash
  python metastate.py build --domain research
  ```

  Verify `dist/research/` has correct structure:
  - `.claude_plugin/plugin.json` with name "research"
  - `skills/planning/SKILL.md` with VERIFIED/UNVERIFIED conditions
  - `skills/executing/SKILL.md` with researcher/fact-checker/methodology-reviewer agents
  - `skills/issue-handling/SKILL.md` with BI/MI/EI issue prefixes
  - `skills/acceptance/SKILL.md` with research verification criteria
  - `agents/*.md` with all 4 research agents

- [ ] **Step 5: Verify research domain is NOT coding-specific**

  Check that the built research plugin has no coding-specific references:
  - No pytest, curl, or other coding tools mentioned
  - No code-specific terminology (implementation, TDD, unit test)
  - File paths use research-specific names (findings.md, verification-results.md, brief.md)
  - Conditions use VERIFIED/UNVERIFIED, not EXPECTED/UNEXPECTED