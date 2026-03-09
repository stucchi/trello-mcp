# Trello MCP Server

[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/trello-mcp)](https://pypi.org/project/trello-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An MCP server for the Trello REST API. Manage boards, lists, cards, labels, checklists, and more from any MCP-compatible client.

## Tools

| Tool | Description |
|------|-------------|
| `list_my_boards` | List all boards for the authenticated user |
| `get_board` | Get details of a single board |
| `get_board_lists` | Get all lists on a board |
| `create_list` | Create a new list on a board |
| `get_list_cards` | Get all cards in a list |
| `get_board_cards` | Get all cards on a board |
| `get_card` | Get details of a single card |
| `create_card` | Create a new card in a list |
| `update_card` | Update one or more fields on a card |
| `move_card` | Move a card to a different list/board |
| `archive_card` | Archive (close) a card |
| `get_card_comments` | Get all comments on a card |
| `add_card_comment` | Add a comment to a card |
| `get_card_attachments` | Get all attachments on a card |
| `add_card_attachment` | Upload a file as an attachment to a card |
| `add_card_url_attachment` | Attach a URL to a card |
| `delete_card_attachment` | Delete an attachment from a card |
| `get_board_labels` | Get all labels on a board |
| `create_label` | Create a label on a board |
| `get_card_checklists` | Get all checklists on a card |
| `get_checklist` | Get a checklist and its items |
| `create_checklist` | Create a checklist on a card |
| `add_checklist_item` | Add an item to a checklist |
| `get_me` | Get the authenticated member's profile |
| `search_trello` | Search for cards and/or boards |
| `get_card_history` | Get the action history of a card (moves, edits, comments, etc.) |

## Prerequisites

1. Go to [trello.com/power-ups/admin](https://trello.com/power-ups/admin) and create a new Power-Up
2. Copy your **API Key**
3. Generate a **Token** using the link on the same page

## Installation

```bash
uvx trello-mcp
```

Or install from PyPI:

```bash
pip install trello-mcp
```

## Usage

### Claude Desktop / Claude Code

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "trello": {
      "command": "uvx",
      "args": ["trello-mcp"],
      "env": {
        "TRELLO_API_KEY": "your-api-key",
        "TRELLO_TOKEN": "your-token"
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|:--------:|-------------|
| `TRELLO_API_KEY` | Yes | API key from Trello Power-Up admin |
| `TRELLO_TOKEN` | Yes | User token generated for your API key |

## Development

```bash
git clone https://github.com/stucchi/trello-mcp.git
cd trello-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT

<!-- mcp-name: io.github.stucchi/trello -->
