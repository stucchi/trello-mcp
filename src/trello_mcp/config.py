from dataclasses import dataclass
import os


@dataclass(frozen=True)
class TrelloConfig:
    api_key: str
    token: str
    base_url: str = "https://api.trello.com/1"

    @staticmethod
    def from_env() -> "TrelloConfig":
        api_key = os.environ.get("TRELLO_API_KEY", "")
        token = os.environ.get("TRELLO_TOKEN", "")

        missing: list[str] = []
        if not api_key:
            missing.append("TRELLO_API_KEY")
        if not token:
            missing.append("TRELLO_TOKEN")

        if missing:
            raise RuntimeError(
                f"Required environment variables missing: {', '.join(missing)}\n"
                "Configure:\n"
                "  TRELLO_API_KEY  – API key from https://trello.com/power-ups/admin\n"
                "  TRELLO_TOKEN    – User token generated for your API key"
            )

        return TrelloConfig(api_key=api_key, token=token)


_config: TrelloConfig | None = None


def get_config() -> TrelloConfig:
    global _config
    if _config is None:
        _config = TrelloConfig.from_env()
    return _config


def reset_config() -> None:
    """Reset the cached config (used in tests)."""
    global _config
    _config = None
