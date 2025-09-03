# 🤖 AGENTS.md - Agent Fetch Tool Guide

## Welcome

**Hello! I'm your AI development assistant for the agent-fetch tool.**

This document provides comprehensive guidance for developers, CI/CD systems, and AI agents working with the agent-fetch tool, including detailed usage examples, configuration options, and troubleshooting guides.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Command Reference](#command-reference)
3. [Configuration Guide](#configuration-guide)
4. [Advanced Usage](#advanced-usage)
5. [Troubleshooting](#troubleshooting)
6. [Integration Examples](#integration-examples)
7. [Best Practices](#best-practices)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd agent-fetch

# Install the tool
pip install -e .
```

### Basic Usage (No Setup Required)

The tool comes pre-configured with a default repository, so it works immediately:

```bash
# Interactive mode (uses default repo automatically)
agentfetch

# Fetch all files automatically
agentfetch main --all

# Fetch specific files with fuzzy search
agentfetch main --name "api"
```

### Using a Different Repository

If you want to use a repository other than the default:

```bash
# Override with --repo flag for one-time use
agentfetch main --all --repo https://github.com/your-org/docs

# Change default repository permanently
agentfetch set-repo https://github.com/your-org/docs
```

### Expected Output

```
📁 Files in index.yaml
Select files to fetch using ↑/↓ arrows, space to select, enter to confirm

❯ Python APIs Guide
  Shadcn UI Components Guide
  Next.js App APIs Guide

3 files selected

Processing...
✓ Python APIs Guide - Success
✓ Shadcn UI Components Guide - Success
✓ Next.js App APIs Guide - Success

Summary: 3/3 files fetched successfully
```

---

## 📚 Command Reference

### Core Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `agentfetch` | Interactive file selection | `agentfetch` |
| `agentfetch --all` | Fetch all files | `agentfetch --all` |
| `agentfetch --name <query>` | Search by fuzzy matching | `agentfetch --name "frontend"` |
| `agentfetch --repo <url>` | Use different repo | `agentfetch --repo https://github.com/org/docs` |
| `agentfetch --branch <branch>` | Specify branch | `agentfetch --branch develop` |
| `agentfetch --no-overwrite` | Skip existing files | `agentfetch --no-overwrite` |

### Configuration Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `agentfetch set-repo <url>` | Set default repository | `agentfetch set-repo https://github.com/org/docs` |
| `agentfetch show-repo` | Display current config | `agentfetch show-repo` |
| `agentfetch list` | List available files | `agentfetch list` |
| `agentfetch validate` | Check repo/index validity | `agentfetch validate` |

### Detailed Command Examples

#### Interactive Mode
```bash
agentfetch
```
Launches a beautiful terminal interface with:
- Arrow key navigation
- Space bar selection
- Enter to confirm
- Fuzzy search support

#### Batch Mode
```bash
# Fetch everything
agentfetch --all

# Target specific repository
agentfetch --all --repo https://github.com/org/templates

# Use specific branch
agentfetch --all --branch feature/new-docs

# Combination
agentfetch --all --repo https://github.com/org/docs --branch main --no-overwrite
```

#### Search Mode
```bash
# Partial matching
agentfetch --name "api"

# Multiple words
agentfetch --name "user manual"

# Case insensitive
agentfetch --name "Frontend Guide"
```

---

## ⚙️ Configuration Guide

### Configuration Location

**Linux/macOS:**
```
~/.agentfetch/config.yaml
```

**Windows:**
```
%APPDATA%\agentfetch\config.yaml
```

### Default Configuration

The tool comes with a pre-configured default repository:

**Default Repo:** `https://github.com/FreeMarketamilitia/agent-fetch`

```bash
# View current configuration to see defaults
agentfetch show-repo

# Expected output:
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Setting    ┃ Value                                                   ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Repository │ https://github.com/FreeMarketamilitia/agent-fetch       │
│ Branch     │ main                                                    │
└────────────┴─────────────────────────────────────────────────────────┘
```

### Custom Configuration

If you want to use a different repository:

```bash
# Set your custom repository
agentfetch set-repo https://github.com/your-organization/documentation
```

**Configuration File Structure:**
```yaml
default_repo: "https://github.com/FreeMarketamilitia/agent-fetch"
default_branch: "main"
```

The configuration file contains user overrides - if you set a custom repo, it will override the default.

### Target Repository Structure

Your target repository must have an `index.yaml` file in the root:

```yaml
agents:
  - name: "Python Development Guide"
    source: "guides/python/AGENTS.md"
    target: "python/AGENTS.md"

  - name: "API Reference"
    source: "docs/api/AGENTS.md"
    target: "api/AGENTS.md"

  - name: "UI Components Guide"
    source: "components/ui/AGENTS.md"
    target: "ui/AGENTS.md"
```

---

## 🔧 Advanced Usage

### CI/CD Integration

#### GitHub Actions Example

```yaml
name: Fetch Documentation
on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  fetch-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install agent-fetch
        run: pip install git+https://github.com/your-org/agent-fetch.git

      - name: Fetch documentation
        run: |
          agentfetch --all --repo https://github.com/your-org/docs

      - name: Commit and push (if changes)
        run: |
          git add .
          if git diff-index --quiet HEAD; then
            echo "No changes to commit"
          else
            git commit -m "Update documentation [auto-fetch]"
            git push
          fi
```

#### Jenkins Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Fetch Docs') {
            steps {
                sh '''
                python3 -m pip install git+https://github.com/your-org/agent-fetch.git
                agentfetch --all --repo https://github.com/your-org/docs
                '''
            }
        }

        stage('Commit Changes') {
            steps {
                sh '''
                git add .
                git commit -m "Update docs [CI]" || echo "No changes"
                git push origin main || echo "No push needed"
                '''
            }
        }
    }
}
```

### Multi-Repository Setup

```bash
#!/bin/bash
# Fetch from multiple repositories

repos=(
    "https://github.com/org/docs:main"
    "https://github.com/org/templates:develop"
    "https://github.com/org/guides:v2.1"
)

for repo in "${repos[@]}"; do
    url=$(echo $repo | cut -d: -f1)
    branch=$(echo $repo | cut -d: -f2)

    echo "Fetching from: $url ($branch)"
    agentfetch --all --repo $url --branch $branch
done
```

### Custom Scripting

```python
#!/usr/bin/env python3
# custom_fetch.py

import subprocess
import pathlib

def fetch_urgent_docs():
    """Fetch only urgent documentation files"""

    # List available files
    result = subprocess.run(['agentfetch', 'list'],
                          capture_output=True, text=True, cwd=pathlib.Path.cwd())

    if result.returncode == 0:
        # Parse output and filter by priority
        priority_files = [
            "Security Guide",
            "API Reference",
            "User Manual"
        ]

        for file in priority_files:
            subprocess.run(['agentfetch', '--name', file])

    return "Urgent docs fetched successfully"

if __name__ == "__main__":
    print(fetch_urgent_docs())
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. "No such option" Error

**Problem:**
```bash
Error: No such option: --all
```

**Solution:**
Use the correct command format:
```bash
# ❌ Wrong
agentfetch --all

# ✅ Correct for basic usage
agentfetch main --all
```

#### 2. Repository Not Found

**Problem:**
```
Error: Repository not found or access denied
```

**Solutions:**
```bash
# Check repository URL
agentfetch validate --repo https://github.com/your-org/repo

# Ensure it's a public repository or you have access token
# Set up authentication if needed
```

#### 3. Configuration Not Found

**Problem:**
```
Error: No default repository configured
```

**Solution:**
```bash
agentfetch set-repo https://github.com/your-org/docs
```

#### 4. Branch Not Found

**Problem:**
```
Error: Branch 'feature/not-found' not found
```

**Solution:**
```bash
# List available branches and choose valid one
agentfetch list --repo https://github.com/org/repo --branch main
```

### Debug Mode

Enable verbose output for troubleshooting:

```bash
# Check repository structure
agentfetch validate --repo https://github.com/your-org/repo

# List all available files
agentfetch list --repo https://github.com/your-org/repo
```

### File Permissions

If you encounter permission issues:
```bash
# On macOS/Linux
chmod +x ~/.agentfetch/config.yaml

# On Windows, ensure proper permissions for %APPDATA%\agentfetch
```

---

## 🔌 Integration Examples

### With Development Workflows

#### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Fetching latest documentation..."
agentfetch --all --no-overwrite

echo "Documentation updated successfully"
```

#### Python Project Integration

```python
# setup_fetch.py
import subprocess
import pathlib

def ensure_docs_are_current():
    """Ensure documentation is up to date before builds"""
    try:
        subprocess.run(['agentfetch', 'main', '--all', '--no-overwrite'],
                      check=True, cwd=pathlib.Path.cwd())
        return True
    except subprocess.CalledProcessError:
        print("Failed to fetch documentation")
        return False

# Use in CI/CD
if __name__ == "__main__":
    if ensure_docs_are_current():
        print("✓ Documentation is current")
    else:
        exit(1)
```

### With Documentation Tools

#### MkDocs Integration

```bash
#!/bin/bash
# docs_update.sh

echo "Step 1: Fetch latest docs"
agentfetch --all

echo "Step 2: Build documentation"
mkdocs build

echo "Step 3: Deploy"
mkdocs gh-deploy
```

#### Sphinx Documentation

```bash
#!/bin/bash
# sphinx_update.sh

echo "Fetching documentation guides"
agentfetch --all --repo https://github.com/your-org/sphinx-docs

echo "Building Sphinx documentation"
make html

echo "Serving documentation"
python -m http.server 8000 --directory _build/html
```

---

## 📋 Best Practices

### Repository Organization

1. **Clear Naming Convention**
   ```yaml
   # Use descriptive names in index.yaml
   agents:
     - name: "REST API Documentation"
       source: "docs/api/rest/AGENTS.md"
       target: "api/rest.md"

     - name: "GraphQL Schema Guide"
       source: "docs/api/graphql/AGENTS.md"
       target: "api/graphql.md"
   ```

2. **Consistent Folder Structure**
   ```
   docs/
   ├── api/
   │   ├── rest/
   │   │   └── AGENTS.md
   │   └── graphql/
   │       └── AGENTS.md
   └── ui/
       └── components/
           └── AGENTS.md
   ```

### CI/CD Recommendations

1. **Schedule Regular Updates**
   ```yaml
   # Daily at 2 AM
   on:
     schedule:
       - cron: '0 2 * * *'
   ```

2. **Conditional Updates**
   ```bash
   # Only update if there are changes in source repo
   agentfetch --all --no-overwrite
   ```

3. **Error Handling**
   ```yaml
   - name: Safe fetch
     run: |
       agentfetch --all --no-overwrite
     continue-on-error: true
   ```

### Team Collaboration

1. **Shared Configuration**
   ```yaml
   # Shared config for team repos
   default_repo: "https://github.com/team/documentation"
   default_branch: "main"
   ```

2. **Documentation Standards**
   - Use consistent naming
   - Include dates/updates
   - Add change history

3. **Access Control**
   - Ensure team members have access to target repositories
   - Use branch protections appropriately

---

## 🎯 Summary

This AGENTS.md guide provides comprehensive documentation for using the agent-fetch tool effectively. Key takeaways:

1. **Installation**: `pip install -e .`
2. **Configuration**: Set up default repository with `agentfetch set-repo`
3. **Basic Usage**:
   - Interactive: `agentfetch`
   - Batch: `agentfetch main --all`
   - Search: `agentfetch main --name "search term"`
4. **Integration**: Easily integrates with CI/CD and development workflows
5. **Best Practices**: Use consistent naming and regular updates

For additional help or issues, please reference the troubleshooting section or open an issue in the project repository.

**Happy fetching! 🚀**
