"""Tests for password authentication in Jira configuration."""

import os
from unittest.mock import patch

import pytest

from mcp_atlassian.jira.config import JiraConfig


class TestJiraPasswordAuth:
    """Test password authentication functionality for Jira."""

    def test_password_takes_priority_over_api_token(self):
        """Test that password is used when both password and api_token are provided."""
        with patch.dict(
            os.environ,
            {
                "JIRA_URL": "https://jira.example.com",
                "JIRA_USERNAME": "testuser",
                "JIRA_PASSWORD": "testpassword", 
                "JIRA_API_TOKEN": "testtoken",
            },
            clear=True,
        ):
            config = JiraConfig.from_env()
            assert config.password == "testpassword"
            assert config.api_token == "testtoken"
            assert config.auth_type == "basic"
            assert config.is_auth_configured()

    def test_password_only_authentication(self):
        """Test authentication with password only (no api_token)."""
        with patch.dict(
            os.environ,
            {
                "JIRA_URL": "https://jira.example.com",
                "JIRA_USERNAME": "testuser",
                "JIRA_PASSWORD": "testpassword",
            },
            clear=True,
        ):
            config = JiraConfig.from_env()
            assert config.password == "testpassword"
            assert config.api_token is None
            assert config.auth_type == "basic"
            assert config.is_auth_configured()

    def test_fallback_to_api_token_when_no_password(self):
        """Test that api_token is used when password is not provided."""
        with patch.dict(
            os.environ,
            {
                "JIRA_URL": "https://jira.example.com",
                "JIRA_USERNAME": "testuser",
                "JIRA_API_TOKEN": "testtoken",
            },
            clear=True,
        ):
            config = JiraConfig.from_env()
            assert config.password is None
            assert config.api_token == "testtoken"
            assert config.auth_type == "basic"
            assert config.is_auth_configured()

    def test_server_dc_password_authentication(self):
        """Test password authentication for Server/Data Center."""
        with patch.dict(
            os.environ,
            {
                "JIRA_URL": "https://jira.internal.com",  # Non-cloud URL
                "JIRA_USERNAME": "testuser",
                "JIRA_PASSWORD": "testpassword",
            },
            clear=True,
        ):
            config = JiraConfig.from_env()
            assert config.password == "testpassword"
            assert config.auth_type == "basic"
            assert not config.is_cloud  # Should be Server/DC
            assert config.is_auth_configured()

    def test_missing_credentials_raises_error(self):
        """Test that missing credentials raise appropriate errors."""
        with patch.dict(
            os.environ,
            {
                "JIRA_URL": "https://example.atlassian.net",  # Cloud URL
                "JIRA_USERNAME": "testuser",
                # Missing both password and api_token
            },
            clear=True,
        ):
            with pytest.raises(ValueError, match="Cloud authentication requires"):
                JiraConfig.from_env()

    def test_is_auth_configured_with_password(self):
        """Test is_auth_configured returns True when password is provided."""
        config = JiraConfig(
            url="https://jira.example.com",
            auth_type="basic",
            username="testuser",
            password="testpassword",
            api_token=None,
        )
        assert config.is_auth_configured()

    def test_is_auth_configured_with_both_credentials(self):
        """Test is_auth_configured returns True when both password and api_token are provided."""
        config = JiraConfig(
            url="https://jira.example.com",
            auth_type="basic",
            username="testuser",
            password="testpassword",
            api_token="testtoken",
        )
        assert config.is_auth_configured()

    def test_is_auth_configured_fails_without_credentials(self):
        """Test is_auth_configured returns False when no password or api_token is provided."""
        config = JiraConfig(
            url="https://jira.example.com",
            auth_type="basic",
            username="testuser",
            password=None,
            api_token=None,
        )
        assert not config.is_auth_configured()