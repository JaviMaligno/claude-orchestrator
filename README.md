# claude-code-orchestrator

Orchestrator for running parallel Claude Code agents on multiple tasks. Each task runs in its own git worktree with a dedicated agent instance.

## Features

- **Parallel Task Execution**: Run multiple Claude Code agents simultaneously on different tasks
- **Git Worktree Isolation**: Each task runs in its own worktree to prevent conflicts
- **Auto-detect Git Provider**: Automatically detects Bitbucket or GitHub from remote URL
- **MCP Integration**: Uses Bitbucket MCP for Bitbucket repos, `gh` CLI for GitHub
- **Extensible MCP Registry**: Configure additional MCPs (Atlassian, Linear, Postgres, Chrome, etc.)
- **Project Discovery**: Automatically analyzes project structure and conventions
- **Task Generation**: Generate task configurations from todo.md files

## Installation

```bash
# With pip
pip install claude-code-orchestrator

# With uv
uv add claude-code-orchestrator

# With pipx (for CLI usage)
pipx install claude-code-orchestrator
```

## Prerequisites

### For GitHub Repositories

```bash
# Install GitHub CLI
brew install gh  # macOS
# or: sudo apt install gh  # Ubuntu

# Authenticate
gh auth login
```

### For Bitbucket Repositories

```bash
# Install Bitbucket MCP
pipx install mcp-server-bitbucket

# Configure MCP
claude mcp add bitbucket -s user \
  -e BITBUCKET_WORKSPACE=your-workspace \
  -e BITBUCKET_EMAIL=your-email \
  -e BITBUCKET_API_TOKEN=your-token \
  -- mcp-server-bitbucket
```

## Quick Start

```bash
# Check prerequisites
claude-orchestrator doctor

# Initialize project configuration
claude-orchestrator init

# Generate tasks from a todo file
claude-orchestrator generate --from-todo todo.md

# Run all tasks
claude-orchestrator run

# Or combine generation and execution
claude-orchestrator run --from-todo todo.md --execute
```

## Configuration

Configuration is loaded from two sources (later overrides earlier):
1. **Global config**: `~/.config/claude-orchestrator/config.yaml`
2. **Project config**: `.claude-orchestrator.yaml`

### Project Configuration

Create `.claude-orchestrator.yaml` in your project root:

```yaml
# Git settings (auto-detected if not specified)
git:
  provider: auto  # "bitbucket" / "github" / auto-detect
  base_branch: develop
  destination_branch: develop
  repo_slug: my-repo  # Required for Bitbucket

worktree_dir: ../worktrees

# MCPs to enable for agents
mcps:
  enabled:
    - atlassian    # For Jira ticket updates
    - linear       # For issue tracking

# Project context (auto-discovered if not specified)
project:
  key_files:
    - src/main.py
    - tests/
  test_command: pytest tests/
```

### Global Configuration

Set defaults that apply to all projects:

```bash
# Set global default base branch
claude-orchestrator config --global git.base_branch develop

# View global config
claude-orchestrator config --global --list
```

Global config is stored in `~/.config/claude-orchestrator/config.yaml`.

## CLI Commands

### `doctor`

Check all prerequisites and configuration:

```bash
claude-orchestrator doctor
```

Output:
```
✓ Git provider: GitHub (github.com detected)
✓ gh CLI: installed and authenticated
✓ MCP atlassian: configured
✗ MCP linear: not configured
  Run: pipx install mcp-server-linear && claude mcp add linear...
```

### `init`

Initialize project configuration:

```bash
claude-orchestrator init
```

This will:
1. Detect git provider
2. Analyze project structure
3. Create `.claude-orchestrator.yaml`

### `generate`

Generate task configuration from a todo file:

```bash
claude-orchestrator generate --from-todo todo.md
```

### `config`

Get or set configuration values (similar to `git config` or `gh config`):

```bash
# List all configuration (merged: global + project)
claude-orchestrator config --list

# Get a specific value
claude-orchestrator config git.base_branch

# Set a project-level value
claude-orchestrator config git.base_branch develop

# Set a global value (applies to all projects)
claude-orchestrator config --global git.base_branch develop
```

Available keys:
- `git.provider` - Git provider ("auto", "github", "bitbucket")
- `git.base_branch` - Base branch for PRs
- `git.destination_branch` - Target branch for PRs
- `git.repo_slug` - Repository slug (Bitbucket)
- `worktree_dir` - Directory for git worktrees
- `project.test_command` - Test command to run
- `mcps.enabled` - Comma-separated list of MCPs
- `workflow.mode` - Workflow mode ("review" or "yolo")
- `workflow.auto_approve` - Auto-approve agent actions (true/false)
- `workflow.auto_pr` - Create PRs automatically (true/false)
- `workflow.stop_after_generate` - Stop after generating tasks (true/false)

### `run`

Execute tasks:

```bash
# Run all tasks (from existing task_config.yaml)
claude-orchestrator run

# Run specific tasks
claude-orchestrator run --tasks task1,task2

# Generate from todo, stop for review (default)
claude-orchestrator run --from-todo todo.md

# Generate and execute without stopping
claude-orchestrator run --from-todo todo.md --execute

# YOLO: Generate, execute, and create PRs without stopping
claude-orchestrator run --from-todo todo.md --yolo

# Auto-approve all agent actions
claude-orchestrator run --auto-approve
```

### `yolo`

Shortcut for full YOLO mode:

```bash
# Generate tasks, execute, and create PRs in one go
claude-orchestrator yolo TODO.md

# Equivalent to:
claude-orchestrator run --from-todo TODO.md --yolo
```

## Workflow Modes

Configure how much the orchestrator stops for review:

| Mode | Description |
|------|-------------|
| `review` (default) | Stop after generating tasks for review |
| `yolo` | Run everything without stopping |

### Configure via CLI

```bash
# Set workflow mode globally
claude-orchestrator config --global workflow.mode yolo

# Or per-project
claude-orchestrator config workflow.mode yolo

# Enable auto-approve (agents won't ask for confirmation)
claude-orchestrator config workflow.auto_approve true

# Disable automatic PR creation
claude-orchestrator config workflow.auto_pr false
```

### Configure in `.claude-orchestrator.yaml`

```yaml
workflow:
  mode: yolo           # "review" or "yolo"
  auto_approve: true   # Automatically approve agent actions
  auto_pr: true        # Create PRs automatically
  stop_after_generate: false  # Fine-grained: stop after task generation
```

## Optional MCPs

| MCP | Auth Type | Use Case |
|-----|-----------|----------|
| `atlassian` | OAuth | Jira/Confluence integration |
| `linear` | OAuth | Issue tracking |
| `postgres` | Env vars | Database access |
| `chrome` | Pre-configured | Browser automation |

### Setting up OAuth MCPs

```bash
# Install the MCP
pipx install mcp-server-atlassian

# Add to Claude (first run will open browser for OAuth)
claude mcp add atlassian -s user -- mcp-server-atlassian
```

## License

MIT

