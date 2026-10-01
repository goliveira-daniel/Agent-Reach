# -*- coding: utf-8 -*-
"""Exact versions for every third-party tool the installer touches.

Pins are the latest stable releases published before the fork's base commit
(a19a171, 2026-09-16). Bump them deliberately after reviewing the upstream
changes, and mirror any change in docs/install.md and docs/update.md.
"""

# This hardened fork. Install the package from this tag, never from a branch.
FORK_REPO = "https://github.com/goliveira-daniel/agent-reach"
FORK_REF = "v1.5.0-hardened.1"
FORK_SOURCE = f"git+{FORK_REPO}.git@{FORK_REF}"

# npm (global)
MCPORTER_SPEC = "mcporter@0.13.13"
OPENCLI_SPEC = "@jackwener/opencli@1.8.7"
UNDICI_SPEC = "undici@8.10.2"

# PyPI (pipx / uv tool)
TWITTER_CLI_SPEC = "twitter-cli==0.8.5"
BILIBILI_CLI_SPEC = "bilibili-cli==0.6.2"
YTDLP_SPEC = "yt-dlp[default]==2026.8.19"

# uvx (MCP server run on demand by mcporter)
LINKEDIN_MCP_SPEC = "mcp-server-linkedin@4.24.3"
