# Task 007: Implement metastate scaffold Command

## Project Overview

- **Goal:** Implement the `metastate scaffold --domain <name>` CLI command that generates agent prompts and acceptance skills from domain descriptions using exemplar-driven LLM generation
- **Architecture:** Python CLI that renders generator templates and invokes LLM (or outputs prompts for manual use)
- **Tech Stack:** Python, Jinja2, PyYAML

## Task Objective

Implement the `metastate scaffold` command that reads a domain yaml, finds exemplar agents, renders generator prompts, and outputs complete agent/acceptance prompts.

This is Task 7 of 11.

---

**Files:**
- Modify: `metastate/metastate.py`
- Reference: `core/generators/agent.md.j2`
- Reference: `core/generators/acceptance.md.j2`

- [ ] **Step 1: Implement exemplar selection**

  ```python
  ROLE_EXEMPLARS = {
      'planner': 'coding/planner.md',
      'implementer': 'coding/implementer.md',
      'reviewer': 'coding/spec-reviewer.md',
  }

  def get_exemplar(agent_name: str, domain_name: str) -> str | None:
      """Find best exemplar agent from existing domains."""
      # First, determine role type from agent name or domain config
      # Then find the exemplar from coding domain
      exemplar_path = ROLE_EXEMPLARS.get(role_type)
      if exemplar_path and os.path.exists(f"domains/{exemplar_path}"):
          with open(f"domains/{exemplar_path}") as f:
              return f.read()
      return None
  ```

- [ ] **Step 2: Implement agent prompt generation**

  ```python
  def generate_agent_prompt(domain: dict, agent_name: str, agent_description: str) -> str:
      """Generate agent prompt from description + exemplar."""
      env = Environment(loader=FileSystemLoader('core'))
      template = env.get_template('generators/agent.md.j2')

      exemplar = get_exemplar(agent_name, domain['name'])

      return template.render(
          domain=domain,
          agent_name=agent_name,
          agent_description=agent_description,
          exemplar_content=exemplar or "No exemplar available",
          role_type=determine_role_type(agent_name),
          role_context=get_role_context(agent_name),
      )
  ```

- [ ] **Step 3: Implement acceptance skill generation**

  ```python
  def generate_acceptance_skill(domain: dict) -> str:
      """Generate acceptance skill from domain summary."""
      env = Environment(loader=FileSystemLoader('core'))
      template = env.get_template('generators/acceptance.md.j2')
      return template.render(domain=domain)
  ```

- [ ] **Step 4: Implement self-check validation**

  ```python
  def check_agent_prompt(content: str) -> list[str]:
      """Check generated agent prompt has all required sections."""
      warnings = []
      if '## Iron Law' not in content:
          warnings.append("Missing Iron Law section")
      if '## Response Format' not in content:
          warnings.append("Missing Response Format section")
      if '## Output Files' not in content:
          warnings.append("Missing Output Files section")
      if '## Process Flow' not in content:
          warnings.append("Missing Process Flow section")
      if '## Issue Handling' not in content and '## ' not in content.replace('## Output Files', ''):
          warnings.append("Missing Issue Handling section")
      if 'ORCHESTRATOR READS' not in content:
          warnings.append("Missing ORCHESTRATOR READS markers in Output Files")
      return warnings

  def check_acceptance_skill(content: str) -> list[str]:
      """Check acceptance skill addresses all four mandatory questions."""
      warnings = []
      required_sections = [
          'What counts as correct output',
          'How to verify',
          'What is NOT acceptable',
          'Verification lifecycle',
      ]
      for section in required_sections:
          if section.lower() not in content.lower():
              warnings.append(f"Missing section: {section}")
      return warnings
  ```

- [ ] **Step 5: Wire up cmd_scaffold in metastate.py**

  ```python
  def cmd_scaffold(args):
      """Scaffold domain files from descriptions."""
      domain_name = args.domain
      domain = load_domain(domain_name)

      output_dir = f"domains/{domain_name}"
      os.makedirs(f"{output_dir}/agents", exist_ok=True)
      os.makedirs(f"{output_dir}/skills", exist_ok=True)

      # Generate agent prompts
      all_agents = {}
      agents_config = domain['agents']
      all_agents['planner'] = agents_config['planner']
      all_agents['implementer'] = agents_config['implementer']
      for reviewer in agents_config.get('plan_reviewers', []):
          all_agents[reviewer] = reviewer
      for reviewer in agents_config.get('reviewers', []):
          all_agents[reviewer] = reviewer

      for agent_name, desc in agents_config.get('agent_descriptions', {}).items():
          prompt = generate_agent_prompt(domain, agent_name, desc)
          warnings = check_agent_prompt(prompt)
          agent_file = f"{output_dir}/agents/{agent_name}.md"
          with open(agent_file, 'w') as f:
              f.write(prompt)
          print(f"Generated {agent_file}")
          for w in warnings:
              print(f"  WARNING: {w}")

      # Generate acceptance skill
      acceptance = generate_acceptance_skill(domain)
      warnings = check_acceptance_skill(acceptance)
      acceptance_file = f"{output_dir}/skills/acceptance.md"
      with open(acceptance_file, 'w') as f:
          f.write(acceptance)
      print(f"Generated {acceptance_file}")
      for w in warnings:
          print(f"  WARNING: {w}")
  ```

- [ ] **Step 6: Create research and copywriting domain yamls**

  Create `domains/research.yaml` and `domains/copywriting.yaml` from the design spec examples.

- [ ] **Step 7: Test scaffold for research domain**

  ```bash
  python metastate.py scaffold --domain research
  ```
  Verify generated files pass self-check and have all required sections.