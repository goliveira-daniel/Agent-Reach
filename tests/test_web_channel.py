# -*- coding: utf-8 -*-
"""Tests for the ``web`` channel.

The fork removed the Jina Reader proxy: the channel only points the agent at
its built-in WebFetch/WebSearch tools and never makes network requests.
"""

from unittest.mock import patch

from agent_reach.channels.web import WebChannel


def test_can_handle_accepts_any_url():
    channel = WebChannel()
    for sample in [
        "https://example.com",
        "http://example.com/path?q=1",
        "example.com",
        "not a url at all",
        "",
    ]:
        assert channel.can_handle(sample) is True, sample


def test_check_points_to_builtin_tools_and_touches_no_network():
    channel = WebChannel()
    with patch("urllib.request.urlopen") as mock_open:
        status, message = channel.check()
    assert status == "ok"
    assert channel.active_backend == "Built-in WebFetch"
    assert "WebFetch" in message
    assert "jina" not in message.lower()
    mock_open.assert_not_called()


def test_channel_has_no_third_party_reader():
    assert not hasattr(WebChannel, "read")
