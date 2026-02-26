from typing import Any

from trello_mcp.client import TrelloClient


async def get_checklist(checklist_id: str) -> dict[str, Any]:
    """Return a checklist with its items."""
    client = TrelloClient()
    cl = await client.get(f"/checklists/{checklist_id}")
    return {
        "id": cl["id"],
        "name": cl["name"],
        "card_id": cl.get("idCard", ""),
        "items": [
            {
                "id": item["id"],
                "name": item["name"],
                "state": item["state"],
                "position": item.get("pos"),
            }
            for item in cl.get("checkItems", [])
        ],
    }


async def create_checklist(card_id: str, name: str) -> dict[str, Any]:
    """Create a checklist on a card."""
    client = TrelloClient()
    cl = await client.post(
        f"/cards/{card_id}/checklists",
        params={"name": name},
    )
    return {
        "id": cl["id"],
        "name": cl["name"],
        "card_id": cl.get("idCard", ""),
        "items": [],
    }


async def add_checklist_item(
    checklist_id: str, name: str, checked: bool = False
) -> dict[str, Any]:
    """Add an item to a checklist."""
    client = TrelloClient()
    item = await client.post(
        f"/checklists/{checklist_id}/checkItems",
        params={"name": name, "checked": str(checked).lower()},
    )
    return {
        "id": item["id"],
        "name": item["name"],
        "state": item.get("state", "incomplete"),
        "position": item.get("pos"),
    }
