"""Tests for authentication validator utilities."""

from unittest.mock import Mock, patch

import pytest

from mcp_atlassian.confluence.config import ConfluenceConfig
from mcp_atlassian.jira.config import JiraConfig
from mcp_atlassian.utils.auth_validator import validate_confluence_auth, validate_jira_auth


class TestAuthValidator:
    """Test authentication validation functionality."""

    @patch("mcp_atlassian.utils.auth_validator.JiraClient")
    def test_validate_jira_auth_success(self, mock_jira_client_class):
        """Test successful Jira authentication validation."""
        # Mock the client and its method
        mock_client = Mock()
        mock_client.jira.myself.return_value = {"accountId": "test123"}
        mock_jira_client_class.return_value = mock_client

        config = JiraConfig(
            url="https://jira.example.com",
            auth_type="basic",
            username="testuser",
            password="testpassword",
        )

        result = validate_jira_auth(config)
        
        assert result is True
        mock_jira_client_class.assert_called_once_with(config)
        mock_client.jira.myself.assert_called_once()

    @patch("mcp_atlassian.utils.auth_validator.JiraClient")
    def test_validate_jira_auth_failure(self, mock_jira_client_class):
        """Test failed Jira authentication validation."""
        # Mock the client to raise an exception
        mock_client = Mock()
        mock_client.jira.myself.side_effect = Exception("Authentication failed")
        mock_jira_client_class.return_value = mock_client

        config = JiraConfig(
            url="https://jira.example.com",
            auth_type="basic",
            username="testuser",
            password="wrongpassword",
        )

        result = validate_jira_auth(config)
        
        assert result is False
        mock_jira_client_class.assert_called_once_with(config)
        mock_client.jira.myself.assert_called_once()

    @patch("mcp_atlassian.utils.auth_validator.ConfluenceClient")
    def test_validate_confluence_auth_success(self, mock_confluence_client_class):
        """Test successful Confluence authentication validation."""
        # Mock the client and its method
        mock_client = Mock()
        mock_client.confluence.get_current_user.return_value = {"accountId": "test123"}
        mock_confluence_client_class.return_value = mock_client

        config = ConfluenceConfig(
            url="https://confluence.example.com",
            auth_type="basic",
            username="testuser",
            password="testpassword",
        )

        result = validate_confluence_auth(config)
        
        assert result is True
        mock_confluence_client_class.assert_called_once_with(config)
        mock_client.confluence.get_current_user.assert_called_once()

    @patch("mcp_atlassian.utils.auth_validator.ConfluenceClient")
    def test_validate_confluence_auth_failure(self, mock_confluence_client_class):
        """Test failed Confluence authentication validation."""
        # Mock the client to raise an exception
        mock_client = Mock()
        mock_client.confluence.get_current_user.side_effect = Exception("Authentication failed")
        mock_confluence_client_class.return_value = mock_client

        config = ConfluenceConfig(
            url="https://confluence.example.com",
            auth_type="basic",
            username="testuser",
            password="wrongpassword",
        )

        result = validate_confluence_auth(config)
        
        assert result is False
        mock_confluence_client_class.assert_called_once_with(config)
        mock_client.confluence.get_current_user.assert_called_once()

    @patch("mcp_atlassian.utils.auth_validator.JiraClient")
    def test_validate_jira_auth_with_different_config_types(self, mock_jira_client_class):
        """Test Jira validation with different authentication types."""
        mock_client = Mock()
        mock_client.jira.myself.return_value = {"accountId": "test123"}
        mock_jira_client_class.return_value = mock_client

        # Test with PAT auth
        config = JiraConfig(
            url="https://jira.example.com",
            auth_type="pat",
            personal_token="testtoken123",
        )

        result = validate_jira_auth(config)
        
        assert result is True
        mock_jira_client_class.assert_called_with(config)
        
        # Test with API token auth
        config = JiraConfig(
            url="https://jira.example.com",
            auth_type="basic",
            username="testuser",
            api_token="testtoken123",
        )

        result = validate_jira_auth(config)
        
        assert result is True

    @patch("mcp_atlassian.utils.auth_validator.ConfluenceClient")
    def test_validate_confluence_auth_with_different_config_types(self, mock_confluence_client_class):
        """Test Confluence validation with different authentication types."""
        mock_client = Mock()
        mock_client.confluence.get_current_user.return_value = {"accountId": "test123"}
        mock_confluence_client_class.return_value = mock_client

        # Test with PAT auth
        config = ConfluenceConfig(
            url="https://confluence.example.com",
            auth_type="pat",
            personal_token="testtoken123",
        )

        result = validate_confluence_auth(config)
        
        assert result is True
        mock_confluence_client_class.assert_called_with(config)
        
        # Test with API token auth
        config = ConfluenceConfig(
            url="https://confluence.example.com",
            auth_type="basic",
            username="testuser",
            api_token="testtoken123",
        )

        result = validate_confluence_auth(config)
        
        assert result is True