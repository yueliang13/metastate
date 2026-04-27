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