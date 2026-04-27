# Task 001: Initialize Metastate Project Structure

## Project Overview

- **Goal:** Create the metastate framework — a domain-agnostic state machine orchestrator that extracts superteam's pattern into reusable skeleton + pluggable domain meat
- **Architecture:** Jinja2 templates for skeleton, domain yaml for meat, `metastate build` and `metastate scaffold` CLI commands
- **Tech Stack:** Python, Jinja2, PyYAML

## Task Objective

Initialize the metastate project at `/Users/yue/Code/Skill/metastate/` with the complete directory structure and CLI entry point.

This is Task 1 of 11.

---

**Files:**
- Create: `metastate/metastate.py` — CLI entry point with `build` and `scaffold` subcommands
- Create: `metastate/requirements.txt` — Python dependencies (jinja2, pyyaml)
- Create: `metastate/.gitignore` — ignore dist/ and __pycache__
- Create: `metastate/README.md` — project overview
- Create: `metastate/core/` — directory structure (orchestrators/, agents/, skills/, generators/)
- Create: `metastate/domains/` — directory structure
- Create: `metastate/dist/` — build output directory (gitignored)
- Create: `metastate/.claude_plugin/plugin.json` — minimal plugin manifest

- [ ] **Step 1: Create project directories**
  ```bash
  mkdir -p metastate/core/{orchestrators,agents,skills,generators}
  mkdir -p metastate/dist
  mkdir -p metastate/domains
  ```

- [ ] **Step 2: Create metastate.py CLI skeleton**
  ```python
  #!/usr/bin/env python3
  """Metastate CLI — domain-agnostic state machine framework."""
  import argparse
  import sys

  def cmd_build(args):
      """Build a Claude Code plugin from domain config."""
      # TODO: implement
      print(f"Building domain: {args.domain}")

  def cmd_scaffold(args):
      """Scaffold agent prompts and acceptance skills from domain config."""
      # TODO: implement
      print(f"Scaffolding domain: {args.domain}")

  def main():
      parser = argparse.ArgumentParser(description="Metastate CLI")
      subparsers = parser.add_subparsers(dest="command", required=True)

      build_parser = subparsers.add_parser("build", help="Build plugin from domain")
      build_parser.add_argument("--domain", required=True, help="Domain name")
      build_parser.set_defaults(func=cmd_build)

      scaffold_parser = subparsers.add_parser("scaffold", help="Scaffold domain files")
      scaffold_parser.add_argument("--domain", required=True, help="Domain name")
      scaffold_parser.set_defaults(func=cmd_scaffold)

      args = parser.parse_args()
      args.func(args)

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 3: Create requirements.txt**
  ```
  jinja2>=3.1
  pyyaml>=6.0
  ```

- [ ] **Step 4: Create .gitignore**
  ```
  dist/
  __pycache__/
  *.pyc
  .DS_Store
  ```

- [ ] **Step 5: Create .claude_plugin/plugin.json**
  ```json
  {
    "name": "metastate",
    "description": "Domain-agnostic state machine framework for AI-driven workflows",
    "version": "0.1.0",
    "author": {
      "name": "FW Lei"
    }
  }
  ```

- [ ] **Step 6: Initialize git repo**
  ```bash
  cd /Users/yue/Code/Skill/metastate && git init && git add -A && git commit -m "Initialize metastate project structure"
  ```

- [ ] **Step 7: Verify structure**
  ```bash
  tree /Users/yue/Code/Skill/metastate -I '.git'
  ```