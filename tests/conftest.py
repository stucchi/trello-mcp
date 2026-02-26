import pytest

from trello_mcp.config import reset_config


@pytest.fixture(autouse=True)
def _trello_env(monkeypatch):
    monkeypatch.setenv("TRELLO_API_KEY", "test-key")
    monkeypatch.setenv("TRELLO_TOKEN", "test-token")
    reset_config()
    yield
    reset_config()
