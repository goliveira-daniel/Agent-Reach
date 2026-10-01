# Agent Reach — Update Guide (hardened fork)

This fork is pinned. Nothing updates itself, and an agent must never fetch
update instructions or code from a moving branch. Updating is a reviewed,
manual change to the fork.

## For Humans

1. Check what upstream changed since the current base:
   ```bash
   cd ~/src/agent-reach
   git fetch https://github.com/Panniantong/agent-reach.git main
   git log --oneline HEAD..FETCH_HEAD
   git diff HEAD...FETCH_HEAD -- agent_reach/skill docs agent_reach/cli.py
   ```
2. Review the diff (skill text, install commands, new network calls).
3. Merge what you accept into the `hardening` branch, run
   `pytest tests/ -v`, and update `agent_reach/pins.py` plus the pin table in
   `docs/install.md` for any tool version you bump.
4. Tag the reviewed commit (for example `v1.5.0-hardened.2`), set `FORK_REF` in
   `agent_reach/pins.py` to it, and push the branch and tag to the fork.
5. Reinstall from the local checkout at that tag (Step 2 below).

## For AI Agents

Only run this when the user asks to apply an update they have already
reviewed. Never upgrade a tool to a version that is not in
`agent_reach/pins.py`.

### Workspace Rules

**Never create files, clone repos, or run commands in the agent workspace.** Use `/tmp/` for temporary work and `~/.agent-reach/` for persistent data.

### Step 1: Check current version

```bash
agent-reach version
agent-reach check-update   # informational only; never installs anything
```

### Step 2: Reinstall the package from the reviewed tag

```bash
git -C ~/src/agent-reach fetch --tags
git -C ~/src/agent-reach checkout v1.5.0-hardened.1   # the tag the user names
pipx install --force ~/src/agent-reach --pip-args="-c $HOME/src/agent-reach/constraints.txt"
```

### Step 3: Re-pin upstream tools that are already installed

Only touch tools that are already installed; do not install new ones.

```bash
# Python-based CLIs (exact versions from agent_reach/pins.py)
which twitter >/dev/null 2>&1 && { pipx install --force 'twitter-cli==0.8.5' 2>/dev/null || uv tool install --force 'twitter-cli==0.8.5' 2>/dev/null; }
which bili    >/dev/null 2>&1 && { pipx install --force 'bilibili-cli==0.6.2' 2>/dev/null || uv tool install --force 'bilibili-cli==0.6.2' 2>/dev/null; }
which yt-dlp  >/dev/null 2>&1 && { pipx install --force 'yt-dlp[default]==2026.8.19' 2>/dev/null || uv tool install --force 'yt-dlp[default]==2026.8.19' 2>/dev/null || python -m pip install 'yt-dlp[default]==2026.8.19' 2>/dev/null; }

# Git-pinned CLIs (same commits as the code)
which rdt  >/dev/null 2>&1 && pipx install --force 'git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66' 2>/dev/null
which boss >/dev/null 2>&1 && pipx install --force 'git+https://github.com/can4hou6joeng4/boss-agent-cli.git@4c991b77086a203173bf08a4cb64a23af6514fe6' 2>/dev/null

# npm-based (exact versions)
which mcporter >/dev/null 2>&1 && npm install -g mcporter@0.13.13 2>/dev/null
which opencli  >/dev/null 2>&1 && npm install -g @jackwener/opencli@1.8.7 2>/dev/null
```

LinkedIn runs through `uvx mcp-server-linkedin@4.24.3`; if the user's
mcporter config still says `@latest`, re-add it:

```bash
mcporter config add linkedin --command uvx --arg mcp-server-linkedin@4.24.3 --env UV_HTTP_TIMEOUT=300 --scope home
```

### Step 4: Refresh the skill (only if the user asks)

`agent-reach doctor` never installs or updates the skill. To refresh it:

```bash
agent-reach skill --install --force   # backs up the old folder, writes ~/.claude/skills/agent-reach
```

### Step 5: Verify and report

```bash
agent-reach version
agent-reach doctor
```

Tell the user the installed version, which channels are available and
through which backend, and anything that needs their action.
