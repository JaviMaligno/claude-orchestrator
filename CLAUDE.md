# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

Claude Orchestrator is a Python package for running parallel Claude Code agents on multiple tasks. Each task runs in its own git worktree with a dedicated agent instance.

## Key Features

- **Parallel Task Execution**: Run multiple Claude Code agents simultaneously
- **Git Worktree Isolation**: Each task runs in its own worktree to prevent conflicts
- **Auto-detect Git Provider**: Automatically detects Bitbucket or GitHub from remote URL
- **MCP Integration**: Uses Bitbucket MCP for Bitbucket repos, `gh` CLI for GitHub
- **Extensible MCP Registry**: Configure additional MCPs (Atlassian, Linear, Postgres, Chrome, etc.)
- **Project Discovery**: Automatically analyzes project structure and conventions

## Development Commands

```bash
# Install dependencies with uv
uv sync

# Or with dev dependencies
uv sync --all-extras

# Run CLI
uv run claude-orchestrator --help
uv run claude-orchestrator doctor
uv run claude-orchestrator init

# Run tests
uv run pytest tests/

# Build and publish
uv build
uv publish
```

## Architecture

### Core Modules

- `cli.py` - Typer-based CLI with commands: doctor, init, generate, run, status
- `orchestrator.py` - Main orchestration logic for running parallel agents
- `git_provider.py` - Auto-detect Bitbucket/GitHub, verify gh CLI or Bitbucket MCP
- `mcp_registry.py` - Extensible registry of MCPs with auth types
- `discovery.py` - Project analysis via Claude for dynamic context
- `task_generator.py` - Generate task configs from todo.md files
- `config.py` - Handle .claude-orchestrator.yaml configuration

### Git Provider Detection

| Provider | Detection | Tool | Auth Check |
|----------|-----------|------|------------|
| GitHub | `github.com` in remote | `gh` CLI | `gh auth status` |
| Bitbucket | `bitbucket.org` in remote | mcp-server-bitbucket | `claude mcp list` |

### MCP Auth Types

| Type | Description | Examples |
|------|-------------|----------|
| `env_vars` | Simple environment variables | bitbucket, postgres |
| `oauth_browser` | Browser OAuth flow | atlassian, linear |
| `pre_configured` | No auth, just check prereqs | chrome, filesystem |

## Configuration

Project configuration is stored in `.claude-orchestrator.yaml`:

```yaml
git:
  provider: auto  # "bitbucket" / "github" / auto-detect
  base_branch: main
  destination_branch: main

worktree_dir: ../worktrees

mcps:
  enabled:
    - atlassian
    - linear

project:
  key_files:
    - src/main.py
  test_command: pytest tests/
```

## Adding New MCPs

To add a new MCP to the registry, update `mcp_registry.py`:

```python
MCP_REGISTRY["new-mcp"] = MCPDefinition(
    name="new-mcp",
    package="mcp-server-new",
    auth_type=AuthType.ENV_VARS,
    env_vars=["NEW_MCP_TOKEN"],
    setup_instructions="..."
)
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `doctor` | Check prerequisites and configuration |
| `init` | Initialize project configuration |
| `generate` | Generate task config from todo.md |
| `run` | Execute tasks with Claude agents |
| `status` | Show results of last run |

## Publishing

```bash
# Build
uv build

# Publish to PyPI
uv publish
```

