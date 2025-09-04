<!-- Hero -->
<div align="center">
  <h1>🚀 agent-fetch</h1>
  <p><strong>A beautiful, interactive CLI to collect AGENTS.md and other docs from GitHub repositories.</strong></p>

  <p>
    <img alt="Platform" src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-2ea44f?style=for-the-badge">
    <img alt="Interface" src="https://img.shields.io/badge/interface-interactive-7b68ee?style=for-the-badge">
    <img alt="Language" src="https://img.shields.io/badge/language-python-blue?style=for-the-badge">
  </p>

  <p>
    <a href="#-features">Features</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-commands">Commands</a> •
    <a href="#-configuration">Configuration</a> •
    <a href="#-index-file-specification">Index Spec</a> •
    <a href="#-example-workflows">Workflows</a> •
    <a href="#-development">Development</a> •
    <a href="#-license">License</a>
  </p>
</div>

<br />

<!-- Intro -->
<p align="center">
  agent-fetch makes it effortless to <strong>discover, fetch, and update</strong> distributed documentation like <code>AGENTS.md</code> across monorepos or multiple projects — perfect for developers and coding agents alike.
</p>

<!-- Highlights -->
<h2 id="-features">✨ Features</h2>

<table>
  <tr>
    <td>🎛️ <strong>Interactive-first</strong><br/>Launch straight into a selection UI with fuzzy search.</td>
    <td>⚙️ <strong>Flexible Automation</strong><br/>Go non-interactive with <code>--all</code>, <code>--name</code>, <code>--repo</code>, and more.</td>
  </tr>
  <tr>
    <td>🧩 <strong>Configurable Defaults</strong><br/>Persist a default repo and override branch per run.</td>
    <td>🎨 <strong>Beautiful Console UI</strong><br/>Colorful prompts powered by <code>questionary</code> and <code>rich</code>.</td>
  </tr>
  <tr>
    <td>🧰 <strong>Well-structured</strong><br/>Clear modules for config, fetching, parsing, UI, and CLI.</td>
    <td>🖥️ <strong>Cross‑platform</strong><br/>Works on macOS, Linux, and Windows.</td>
  </tr>
</table>

<!-- Quick Start -->
<h2 id="-quick-start">🎯 Quick Start</h2>

<details open>
<summary><strong>Install</strong></summary>

```bash
uv tool install agent-fetch
# or
pip install agent-fetch
```

</details>

<details open>
<summary><strong>Run interactive mode</strong></summary>

```bash
# Interactive selection using the configured/default repo
agentfetch main
```

</details>

<details>
<summary><strong>Change default repository (optional)</strong></summary>

```bash
# Persist a default repo in your config file
agentfetch set-repo https://github.com/your-org/docs
```

</details>

<!-- Preview -->
<h3>Expected interactive preview</h3>

```
📁 Files in index.yaml
Select files to fetch using ↑/↓ arrows, space to select, enter to confirm

❯ Python APIs Guide
  Shadcn UI Components Guide
  Next.js App APIs Guide
```

<!-- Commands -->
<h2 id="-commands">📋 Commands</h2>

<p><strong>Executable:</strong> <code>agentfetch</code> (entry point for the Typer app)</p>

<h3>Subcommands</h3>

<table>
  <thead>
    <tr>
      <th>Subcommand</th>
      <th>Description</th>
      <th>Common Options</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>main</code></td>
      <td>Interactive fetcher and batch options</td>
      <td>
        <code>--all</code> •
        <code>--name TEXT</code> •
        <code>--repo URL</code> •
        <code>--branch TEXT</code> •
        <code>--no-overwrite</code>
      </td>
    </tr>
    <tr>
      <td><code>list</code></td>
      <td>List entries from <code>index.yaml</code></td>
      <td>
        <code>--repo URL</code> •
        <code>--branch TEXT</code>
      </td>
    </tr>
    <tr>
      <td><code>validate</code></td>
      <td>Validate <code>index.yaml</code> exists and is well-formed</td>
      <td>
        <code>--repo URL</code> •
        <code>--branch TEXT</code>
      </td>
    </tr>
    <tr>
      <td><code>set-repo</code></td>
      <td>Persist a default repository URL</td>
      <td>
        <code>URL</code> (positional)
      </td>
    </tr>
    <tr>
      <td><code>show-repo</code></td>
      <td>Show current default repository and branch</td>
      <td>—</td>
    </tr>
  </tbody>
</table>

<h3><code>main</code> options (from the actual CLI)</h3>

```bash
agentfetch main [OPTIONS]

Options:
  --all                       Fetch all files defined in index.yaml
  --name TEXT                 Fetch one file by name (supports fuzzy matching)
  --repo TEXT                 Alternate repository URL to fetch from
  --branch TEXT               Branch name to fetch from
  --no-overwrite              Skip existing files instead of overwriting
  --help                      Show this message and exit
```

<h3>Top-level help</h3>

```bash
agentfetch --help
# Shows available subcommands:
# main, list, validate, set-repo, show-repo
```

<!-- Usage Examples -->
<h2>🧪 Usage Examples</h2>

```bash
# Interactive mode (default behavior of the "main" subcommand)
agentfetch main

# Fetch all files from the configured/default repo
agentfetch main --all

# Search by name (fuzzy)
agentfetch main --name "api"

# Override repository and/or branch for this run
agentfetch main --all --repo https://github.com/org/docs --branch develop

# List entries (non-interactive)
agentfetch list --repo https://github.com/org/docs --branch main

# Validate index.yaml in a repo/branch
agentfetch validate --repo https://github.com/org/docs --branch main

# Persist default repository for future runs
agentfetch set-repo https://github.com/your-org/docs

# Inspect current defaults
agentfetch show-repo
```

<!-- Configuration -->
<h2 id="-configuration">🔧 Configuration</h2>
<p>Configuration is stored in:</p>
<ul>
  <li><strong>Linux/macOS</strong>: <code>~/.agentfetch/config.yaml</code></li>
  <li><strong>Windows</strong>: <code>%APPDATA%\agentfetch\config.yaml</code></li>
</ul>

<p>Example config:</p>

```yaml
default_repo: "https://github.com/org/agents"
default_branch: "main"
```

<p>Note: This project ships with a sensible default repo in code. If you don’t set one explicitly, the CLI will try that default or require <code>--repo</code> when needed.</p>

<!-- Index Spec -->
<h2 id="-index-file-specification">📁 Index File Specification</h2>
<p>Place an <code>index.yaml</code> at the root of your target repository:</p>

```yaml
agents:
  - name: "Root Guide"           # Human-readable name
    source: "AGENTS.md"          # Repo-relative path
    target: "downloads/root.md"  # Local destination

  - name: "API Guide"
    source: "services/api/AGENTS.md"
    target: "downloads/api.md"
```

<!-- Workflows -->
<h2 id="-example-workflows">🔍 Example Workflows</h2>

<h3>Standard Development Workflow</h3>

```bash
# Set up default repository (optional but recommended)
agentfetch set-repo https://github.com/your-org/docs

# Interactive selection for daily use
agentfetch main

# Automate fetching all docs
agentfetch main --all

# Fetch specific documentation
agentfetch main --name "user guide"
```

<h3>CI/CD Integration</h3>

```bash
# Non-interactive batch operation
agentfetch main --all --repo https://github.com/org/docs --branch main
```

<h3>Multi-Repository Setup</h3>

```bash
# Fetch from a monorepo, override branch
agentfetch main --repo https://github.com/org/monorepo --branch feature/new-docs
```

<!-- Development -->
<h2 id="-development">🛠️ Development</h2>

<p>This tool is modular and easily extensible, following Python best practices with:</p>
<ul>
  <li><strong>OOP Design</strong>: Clean class-based architecture</li>
  <li><strong>Separation of Concerns</strong>: Config, fetching, parsing, UI, and CLI</li>
  <li><strong>Robust Error Handling</strong>: Comprehensive error handling throughout</li>
  <li><strong>Rich UI</strong>: Beautiful, colorful console output</li>
</ul>

<h3>Project Structure</h3>

```
agents_collector/
├── config/              # Configuration management
├── fetcher/             # GitHub fetching logic
├── parser/              # Index file parsing
├── cli/                 # Command-line interface
├── ui/                  # Interactive UI components
└── __init__.py
```

<h3>Dependencies</h3>
<ul>
  <li><code>typer</code> — CLI framework</li>
  <li><code>pyyaml</code> — YAML parsing</li>
  <li><code>requests</code> — HTTP client</li>
  <li><code>questionary</code> — Interactive menus</li>
  <li><code>rapidfuzz</code> — Fuzzy matching</li>
  <li><code>rich</code> — Beautiful console output</li>
</ul>

<!-- Contributing -->
<h2 id="-contributing">🤝 Contributing</h2>
<p>Contributions are welcome! It’s easy to:</p>
<ul>
  <li>Add new fetcher backends (GitLab, local files, etc.)</li>
  <li>Extend interactive selection features</li>
  <li>Add new CLI commands</li>
  <li>Support additional index file formats</li>
</ul>

<!-- License -->
<h2 id="-license">📄 License</h2>
<p>MIT License</p>

<hr />

<!-- Why -->
<h2>🎉 Why agent-fetch?</h2>
<p>
  Keep your documentation synchronized across teams and codebases. agent-fetch simplifies the process of collecting, organizing, and updating distributed <code>AGENTS.md</code> files so developers and agents always work with the latest, consistent knowledge.
</p>

<p align="center">
  <em>Found this useful? Star the repo to support the project!</em> ⭐
</p>
