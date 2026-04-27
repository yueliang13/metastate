

You are generating a metastate acceptance skill. You will produce a complete,
production-ready acceptance skill markdown file that defines verification
and acceptance criteria for the **copywriting** domain.

## Domain Context

Domain: copywriting
Description: Brand copywriting with editorial review

### Acceptance Overview

Copy must meet brand voice guidelines, pass editorial review for clarity and grammar, and align with target audience. No prohibited terms. Verified against style guide checklist.

### Accept/Reject Labels

- Accept (task passes): **APPROVED**
- Reject (task needs rework): **REJECTED**

These labels are the same ones used in the domain's condition configuration
and in agent output files. The orchestrator reads these labels from status
files to make state transitions.

### Issue Categories
- brief (prefix: BI): Brief ambiguity or contradiction — file: working/brief-issues.md
- style (prefix: SI): Style guide issues — file: working/style-issues.md
- env (prefix: EI): Environment issues — file: working/env-issues.md

## Four Mandatory Questions

Your acceptance skill MUST address all four of these questions completely
and concretely. Do not leave any question partially answered.

### Question 1: What counts as correct output?

Define what "done" looks like in this domain. Be specific about:
- What output files must exist and what they must contain
- What quality standards the output must meet
- What completeness criteria must be satisfied
- What the status line must show (APPROVED vs
  REJECTED)

Do not be vague. "Code works correctly" is not acceptable. "All tests pass,
changes.md lists all modified files, and test-results.md shows
APPROVED status" is acceptable.

### Question 2: How do you verify? (concrete methods)

Specify the exact verification steps an agent should follow. Include:
- What commands to run (with exact arguments)
- What files to read and what to check for in them
- What tools to use (e.g., test frameworks, linters, validators)
- What the expected output of each verification step looks like
- Whether verification is automatic (machine-checkable), semi-automatic
  (machine-assisted but needs human judgment), or manual (human-only)

The verification mode for this domain is: **manual**

If automatic: specify exact commands and expected output.
If semi-automatic: specify what machines check and what humans judge.
If manual: specify the exact checklist a human should follow.

### Question 3: What is NOT acceptable? (hard rules)

List concrete, unambiguous rules. If any of these are violated, the output
is REJECTED regardless of any other qualities.

Hard rules should cover:
- Missing required elements (files, sections, fields)
- Quality violations that cannot be waived
- Process violations (skipped steps, untested changes)
- Common shortcuts that compromise output quality

Each rule must be checkable — an agent should be able to determine
definitively whether the rule is violated.

### Question 4: How does verification map to accept/reject status?

Explain the lifecycle of verification:
1. An agent completes its work and writes output files
2. The agent sets the status line to APPROVED or
   REJECTED
3. The orchestrator reads this status line to decide the next state

Define clearly:
- What conditions produce APPROVED — all
  verification checks pass, all required output exists, no hard rule
  violations
- What conditions produce REJECTED — any
  verification check fails, required output is missing, or a hard rule
  is violated
- What happens at the boundary — how to handle partial failures,
  warnings, or edge cases
- How this interacts with the issue lifecycle — Pending issues mean
  REJECTED, Resolved/Don't Fix issues may still
  be APPROVED if the agent addressed them

## Skill Format

The acceptance skill should be structured as a Claude Code skill with
YAML frontmatter and Markdown body. Follow this structure:

```markdown
---
name: acceptance
description: Use when verifying task output meets acceptance criteria
user-invocation: false
---

# Acceptance Criteria

[Clear title reflecting the domain]

[Opening section: brief summary of what this skill verifies]

## Correct Output

[Answer to Question 1: What counts as correct output]

## Verification Methods

[Answer to Question 2: How to verify, with concrete steps]

## Hard Rules

[Answer to Question 3: What is NOT acceptable]

## Accept/Reject Decision

[Answer to Question 4: How verification maps to accept/reject status]

## Acceptable Status

APPROVED — [brief description of what this means]

## Unacceptable Status

REJECTED — [brief description of what this means]
```

## Generation Instructions

1. Read the domain context above carefully — the domain name, description,
   acceptance summary, accept/reject labels, and verification mode.
2. Address all four mandatory questions completely and concretely.
3. Make every verification step specific enough that an agent could execute
   it without interpretation. Avoid "check that it works" — instead write
   "run [command] and verify the output contains [string]".
4. Hard rules must be unambiguous. "Poor quality" is not a hard rule.
   "Missing required section in output file" is a hard rule.
5. The accept/reject decision section must make it crystal clear how the
   status labels map to verification outcomes. There should be no room
   for interpretation.
6. Use the exact labels APPROVED and
   REJECTED throughout — do not substitute
   synonyms or abbreviations.
7. Output ONLY the complete acceptance skill markdown file. No commentary,
   no explanations, no meta-text. Start with the frontmatter `---` and end
   after the last section.

## Output

Produce the complete acceptance.md file now.