"""Tests for git_provider module."""

import pytest

from claude_orchestrator.git_provider import (
    GitProvider,
    detect_provider,
    parse_remote_url,
)


class TestDetectProvider:
    """Tests for detect_provider function."""

    def test_detect_unknown_without_git(self, tmp_path):
        """Test detection in a non-git directory."""
        result = detect_provider(str(tmp_path))
        assert result == GitProvider.UNKNOWN


class TestParseRemoteUrl:
    """Tests for parse_remote_url function."""

    def test_parse_none_without_git(self, tmp_path):
        """Test parsing in a non-git directory."""
        result = parse_remote_url(str(tmp_path))
        assert result is None

