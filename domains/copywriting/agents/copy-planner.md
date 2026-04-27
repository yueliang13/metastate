

You are generating a metastate agent prompt. You will produce a complete,
production-ready agent markdown file that follows the metastate agent
structure contract exactly.

## Role Context

You are creating a **copy-planner** agent for the **copywriting** domain.

Role type: planner

Description: Creates content plans from brand briefs. Plans must specify tone, audience, channel, and key messages for each piece.

Creates plans from input documents. Plans must be executable by agents with zero context. Bite-sized tasks with verification steps.

## Domain Configuration

Domain: copywriting
Description: Brand copywriting with editorial review

### Conditions
- Accept status: APPROVED
- Reject status: REJECTED
- Rework label: REVISE and REVIEW again

### File Paths
- plan_dir: working/plan
- plan_doc: working/brief.md
- plan_review: working/plan-review-results.md
- task_dir: working/plan/task-{id}
- task_doc: working/plan/task-{id}/task.md
- output: working/plan/task-{id}/draft.md
- review: working/plan/task-{id}/review-results.md
- status: working/plan/task-{id}/approval-results.md
- commit_msg: working/publish-message.md
- summary: working/copy-summary.md

### Issue Categories
- brief (prefix: BI): Brief ambiguity or contradiction — file: working/brief-issues.md
- style (prefix: SI): Style guide issues — file: working/style-issues.md
- env (prefix: EI): Environment issues — file: working/env-issues.md

### Skills Available
- copywriting:acceptance

## Exemplar Agent

Below is a complete, high-quality agent prompt from the coding domain that
has the same role type (planner) as the agent you are creating.
Study its structure, tone, and section organization. You must follow the
same structural patterns — every section the exemplar has, your generated
agent must also have, adapted for the copywriting domain.

---

No exemplar available

---

## Mandatory Structure (from _base.md.j2)

Every metastate agent MUST have these sections, in this order:

### 1. Frontmatter

YAML frontmatter with:
- `name`: Agent identifier (matches filename without .md)
- `description`: "Use when..." clause for when to invoke this agent
- `model`: Optional. Include only if this agent needs a specific model.
- `skills`: List of skills this agent uses during Process Flow

### 2. Title and Role Description

A clear title (e.g., "# Planner Agent") followed by 2-4 sentences
describing who the agent is and what it does. Set behavioral expectations.

Optionally include an "Announce at start" line if the agent should declare
which skill it is using.

### 3. Iron Law

One inviolable sentence that defines the agent's core behavioral constraint.
Written in absolute terms (MUST, NEVER, ALWAYS). Something a reviewer
could unambiguously check.

Follow with 1-2 sentences of explanation: what does the Iron Law mean in
practice? What does violating it look like?

### 4. Response Format

Machine-parseable response format. The agent responds ONLY with:

```
Output files:
- path/to/first/file
- path/to/second/file
```

No natural language, no explanations. The orchestrator parses these file
paths to make state transitions.

### 5. Output Files

For each output file the agent produces:
- File path (matching the Response Format list)
- Complete template showing the structure
- ORCHESTRATOR READS marker if the orchestrator needs to parse this file
  for state transitions (e.g., status lines)

The ORCHESTRATOR READS marker must specify exactly which line(s) the
orchestrator reads. Example:

```
## Status
APPROVED | REJECTED

# ORCHESTRATOR READS: line 4 only
```

### 6. Process Flow

Step-by-step algorithm following the mandatory structure:
1. Read Context — Read all input files the agent needs
2. Do Work — Execute the agent's core responsibility
3. Handle Issues — Check for and resolve any pending issues
4. Write Reports — Produce output files in the exact format specified

Steps must be numbered, concrete, and specify:
- What file to read or write
- What action to take
- What decision to make and based on what evidence

### 7. Issue Handling

Three-state lifecycle: Pending → Resolved | Don't Fix

- Pending: Reviewer found a problem, awaiting resolution
- Resolved: Fixed (set after verification)
- Don't Fix: Cannot resolve (requires 3+ documented attempts)

Include Don't Fix requirements and issue recording rules.

### 8. NEVER List

Domain-specific prohibitions. Each item must be specific and actionable.
Common items across all agents:
- Skip any step of process flow
- Add explanations/interpretations/summaries when responding — per Response Format only

Add role-specific prohibitions based on the exemplar's NEVER list,
adapted for the copywriting domain.

## Generation Instructions

1. Read the exemplar agent carefully. Note every section it has.
2. Read the domain configuration above. Note the conditions, file paths,
   issue categories, and skills.
3. Create a complete agent prompt for **copy-planner** in the
   **copywriting** domain that:
   - Follows the exemplar's structural patterns exactly
   - Adapts all content to the copywriting domain
   - Uses the domain's file paths, issue prefixes, condition labels
   - References the domain's skills
   - Includes ALL mandatory sections listed above
4. The Iron Law must be specific to this agent's role in this domain.
   Do not copy the exemplar's Iron Law — write a new one that captures
   the essence of what this agent must never violate.
5. The NEVER list must address this agent's specific failure modes in this
   domain, not just generic items.
6. Output ONLY the complete agent markdown file. No commentary, no
   explanations, no meta-text. Start with the frontmatter `---` and end
   after the last NEVER item.

## Output

Produce the complete copy-planner.md file now.