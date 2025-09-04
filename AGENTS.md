# 🤖 AGENTS.md — LLM Operations Guide for agent-fetch

This document teaches an LLM how to operate the agent-fetch CLI safely and effectively across interactive, batch, and CI contexts. It reflects the actual command surface implemented in [agents_collector/cli/cli_main.py](agents_collector/cli/cli_main.py) and key behaviors in [python.def main()](agents_collector/cli/cli_main.py:151), [python.def list()](agents_collector/cli/cli_main.py:203), [python.def validate()](agents_collector/cli/cli_main.py:222), [python.def set_repo()](agents_collector/cli/cli_main.py:252), and [python.def show_repo()](agents_collector/cli/cli_main.py:269).

---

## 0) Principles for Autonomous Use

- Prefer deterministic, non-interactive commands in automation. Use interactive selection only for human-in-the-loop workflows.
- Always validate the target repository before fetching when possible.
- Use explicit repository/branch overrides in CI to avoid relying on user config.
- Read output and handle partial success; do not assume all files fetched.
- Respect existing files. Note: current implementation appends if the target file exists (see Implementation Notes).

---

## 1) Install and Entry Point

- Install: 

```bash
uv tool install agent-fetch
# or
pip install agent-fetch
```

- Entry point executable: `agentfetch` (Typer application)
- Interactive and batch operations are exposed under the `main` subcommand.

Tip: `agentfetch --help` lists subcommands. Use `agentfetch main --help` for the fetching options.

---

## 2) Quick Start (LLM-safe)

- Interactive selection (human-in-the-loop):

```bash
agentfetch main
```

- Fetch everything from the configured/default repo:

```bash
agentfetch main --all
```

- Fetch by fuzzy name:

```bash
agentfetch main --name "api"
```

- One-off use with different repo/branch:

```bash
agentfetch main --all --repo https://github.com/org/docs --branch main
```

- Persist a default repo for future runs:

```bash
agentfetch set-repo https://github.com/your-org/docs
```

- Show current defaults:

```bash
agentfetch show-repo
```

---

## 3) Commands and Options (ground truth)

These commands are defined in [agents_collector/cli/cli_main.py](agents_collector/cli/cli_main.py). The fetching surface is implemented in [python.def main()](agents_collector/cli/cli_main.py:151).

- Fetcher: `agentfetch main [OPTIONS]`
  - `--all` — Fetch all files defined in index.yaml
  - `--name TEXT` — Fetch one file by name (fuzzy matching)
  - `--repo TEXT` — Alternate repository URL to fetch from
  - `--branch TEXT` — Branch name to fetch from
  - `--no-overwrite` — Skip existing files instead of overwriting (see notes)

- List entries: `agentfetch list [--repo TEXT] [--branch TEXT]` → [python.def list()](agents_collector/cli/cli_main.py:203)
- Validate repository/index: `agentfetch validate [--repo TEXT] [--branch TEXT]` → [python.def validate()](agents_collector/cli/cli_main.py:222)
- Set default repo: `agentfetch set-repo URL` → [python.def set_repo()](agents_collector/cli/cli_main.py:252)
- Show defaults: `agentfetch show-repo` → [python.def show_repo()](agents_collector/cli/cli_main.py:269)

---

## 4) Configuration

- Location:
  - macOS/Linux: `~/.agentfetch/config.yaml`
  - Windows: `%APPDATA%\agentfetch\config.yaml`

- Defaults are defined in [python.def _get_default_config()](agents_collector/config/config_manager.py:178):

```yaml
default_branch: "main"
default_repo: "https://github.com/FreeMarketamilitia/awesome-agents-md"
```

- Commands:

```bash
agentfetch set-repo https://github.com/your-organization/documentation
agentfetch show-repo
```

---

## 5) Required Repository Structure (target)

The target repository must include an `index.yaml` in its root with entries like:

```yaml
agents:
  - name: "Root Guide"
    source: "AGENTS.md"
    target: "downloads/root.md"
  - name: "API Guide"
    source: "services/api/AGENTS.md"
    target: "downloads/api.md"
```

---

## 6) End-to-End Playbooks

A) Fetch all files deterministically from a specific repo/branch:

```bash
agentfetch validate --repo https://github.com/org/docs --branch main
agentfetch list --repo https://github.com/org/docs --branch main
agentfetch main --all --repo https://github.com/org/docs --branch main
```

B) Fetch a specific file by fuzzy name:

```bash
agentfetch main --name "user guide" --repo https://github.com/org/docs --branch main
```

C) Human-in-the-loop selection:

```bash
agentfetch main
```

D) CI usage (GitHub Actions step):

```bash
agentfetch main --all --repo https://github.com/org/docs --branch main
```

---

## 7) Output Interpretation

Successful runs print a table followed by a summary, e.g.:

```
Summary: 3/3 files fetched successfully
```

- Treat partial success as non-terminal; proceed to next steps while reporting failures.
- If no entries are selected/found, exit gracefully with a neutral status.

---

## 8) Implementation Notes and Behaviors (for planning)

- Default repo/branch are read via [python.class ConfigManager](agents_collector/config/config_manager.py:14) and [python.def get_default_branch()](agents_collector/config/config_manager.py:153)/[python.def get_default_repo()](agents_collector/config/config_manager.py:137).
- Fetching uses [python.class GitHubFetcher](agents_collector/fetcher/github_fetcher.py:14). Raw file URLs are built by [python.def build_raw_url()](agents_collector/fetcher/github_fetcher.py:65).
- Existing-file behavior: in [python.def fetch_files_from_index()](agents_collector/fetcher/github_fetcher.py:133) files are appended if the target already exists:

```python
append_mode = target_path.exists()
```

- The `overwrite` flag propagated from CLI is currently not enforced by the fetcher; plan workflows accordingly (e.g., clean targets before run or choose unique target paths).

---

## 9) Troubleshooting (LLM decision tree)

1) Command returns "No such option":

```bash
# Likely missing the 'main' subcommand
agentfetch main --help
```

2) Validation fails for index.yaml:

```bash
agentfetch validate --repo https://github.com/org/docs --branch main
# If still failing, ensure 'index.yaml' exists at repo root and is publicly accessible.
```

3) No default repository configured:

```bash
agentfetch set-repo https://github.com/your-org/docs
agentfetch show-repo
```

4) Network or 404 fetching a file:

- Confirm the source path in index.yaml is correct for the chosen branch.
- Retry with a known-good file via `--name`.

---

## 10) Examples for Programmatic Use

Python (subprocess) skeleton:

```python
import subprocess, pathlib

def fetch_all(repo, branch="main"):
    subprocess.run(["agentfetch", "validate", "--repo", repo, "--branch", branch], check=True)
    subprocess.run(["agentfetch", "main", "--all", "--repo", repo, "--branch", branch], check=True)

def fetch_by_name(name, repo, branch="main"):
    subprocess.run(["agentfetch", "main", "--name", name, "--repo", repo, "--branch", branch], check=True)
```

Bash loop for multiple repos:

```bash
repos=(
  "https://github.com/org/docs:main"
  "https://github.com/org/templates:develop"
)
for item in "${repos[@]}"; do
  url="${item%%:*}"
  branch="${item##*:}"
  agentfetch main --all --repo "$url" --branch "$branch"
done
```

---

## 11) Summary

- Use `agentfetch main` for interactive and batch fetching.
- Validate and list before fetch in automation.
- Prefer explicit `--repo` and `--branch` in CI.
- Be aware of append-on-existing behavior in the current fetcher.

For human-friendly overview and visuals, see [README.md](README.md).

Happy fetching. 🚀
