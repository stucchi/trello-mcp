import pytest

from trello_mcp.config import TrelloConfig, get_config, reset_config


def test_from_env(monkeypatch):
    monkeypatch.setenv("TRELLO_API_KEY", "my-key")
    monkeypatch.setenv("TRELLO_TOKEN", "my-token")
    reset_config()
    cfg = get_config()
    assert cfg.api_key == "my-key"
    assert cfg.token == "my-token"
    assert cfg.base_url == "https://api.trello.com/1"


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("TRELLO_API_KEY", raising=False)
    monkeypatch.setenv("TRELLO_TOKEN", "my-token")
    reset_config()
    with pytest.raises(RuntimeError, match="TRELLO_API_KEY"):
        TrelloConfig.from_env()


def test_missing_token(monkeypatch):
    monkeypatch.setenv("TRELLO_API_KEY", "my-key")
    monkeypatch.delenv("TRELLO_TOKEN", raising=False)
    reset_config()
    with pytest.raises(RuntimeError, match="TRELLO_TOKEN"):
        TrelloConfig.from_env()


def test_missing_both(monkeypatch):
    monkeypatch.delenv("TRELLO_API_KEY", raising=False)
    monkeypatch.delenv("TRELLO_TOKEN", raising=False)
    reset_config()
    with pytest.raises(RuntimeError, match="TRELLO_API_KEY"):
        TrelloConfig.from_env()


def test_config_is_frozen():
    cfg = TrelloConfig(api_key="k", token="t")
    with pytest.raises(AttributeError):
        cfg.api_key = "other"
