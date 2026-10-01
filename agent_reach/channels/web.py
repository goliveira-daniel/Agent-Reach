# -*- coding: utf-8 -*-
"""Web — generic pages are read with the agent's built-in WebFetch tool.

This fork removed the third-party reader proxy: page URLs are no longer sent
to an external reader service. The channel stays registered so doctor
can tell the agent which tool to use for arbitrary URLs.
"""

from .base import Channel


class WebChannel(Channel):
    name = "web"
    description = "任意网页"
    backends = ["Built-in WebFetch"]
    tier = 0

    def can_handle(self, url: str) -> bool:
        return True  # Fallback — handles any URL

    def check(self, config=None):
        # 无本地命令、不做网络探测，保持零开销
        self.active_backend = self.backends[0]
        return "ok", (
            "通用网页用 Claude Code 内置 WebFetch 读取，网页搜索用内置 WebSearch"
        )
