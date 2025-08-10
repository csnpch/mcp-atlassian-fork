"""Authentication validation utilities for startup checks."""

import logging

from mcp_atlassian.confluence.client import ConfluenceClient
from mcp_atlassian.confluence.config import ConfluenceConfig
from mcp_atlassian.jira.client import JiraClient
from mcp_atlassian.jira.config import JiraConfig

logger = logging.getLogger("mcp-atlassian.auth_validator")


def validate_jira_auth(config: JiraConfig) -> bool:
    """Test Jira authentication by making a simple API call.
    
    Args:
        config: JiraConfig object with authentication credentials
        
    Returns:
        bool: True if authentication is successful, False otherwise
    """
    try:
        client = JiraClient(config)
        # Try multiple endpoints to verify auth (some servers may block certain endpoints)
        try:
            client.jira.myself()
        except Exception:
            # Fallback to server info if myself() is blocked
            client.jira.server_info()
        logger.info("Jira authentication validated successfully")
        return True
    except Exception as e:
        logger.error(f"Jira auth validation failed: {e}")
        return False


def validate_confluence_auth(config: ConfluenceConfig) -> bool:
    """Test Confluence authentication by making a simple API call.
    
    Args:
        config: ConfluenceConfig object with authentication credentials
        
    Returns:
        bool: True if authentication is successful, False otherwise
    """
    try:
        client = ConfluenceClient(config)
        # Try different endpoints to verify auth
        try:
            client.confluence.get_current_user()
        except AttributeError:
            # If get_current_user doesn't exist, try get_current_user_details
            client.confluence.get_current_user_details()
        logger.info("Confluence authentication validated successfully")
        return True
    except Exception as e:
        logger.error(f"Confluence auth validation failed: {e}")
        return False