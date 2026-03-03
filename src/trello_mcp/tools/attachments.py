import os
from typing import Any

from trello_mcp.client import TrelloClient


def _format_attachment(a: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": a["id"],
        "name": a.get("name", ""),
        "url": a.get("url", ""),
        "bytes": a.get("bytes"),
        "mime_type": a.get("mimeType", ""),
        "date": a.get("date", ""),
        "is_upload": a.get("isUpload", False),
    }


async def get_card_attachments(card_id: str) -> list[dict[str, Any]]:
    """Return all attachments on a card."""
    client = TrelloClient()
    attachments = await client.get(f"/cards/{card_id}/attachments")
    return [_format_attachment(a) for a in attachments]


async def add_card_attachment(
    card_id: str,
    file_path: str,
    name: str | None = None,
) -> dict[str, Any]:
    """Upload a file as an attachment to a card."""
    client = TrelloClient()
    file_name = name or os.path.basename(file_path)
    with open(file_path, "rb") as f:
        attachment = await client.post_multipart(
            f"/cards/{card_id}/attachments",
            params={"name": file_name},
            files={"file": (file_name, f)},
        )
    return _format_attachment(attachment)


async def add_card_url_attachment(
    card_id: str,
    url: str,
    name: str | None = None,
) -> dict[str, Any]:
    """Attach a URL to a card."""
    client = TrelloClient()
    params: dict[str, Any] = {"url": url}
    if name:
        params["name"] = name
    attachment = await client.post(f"/cards/{card_id}/attachments", params=params)
    return _format_attachment(attachment)


async def delete_card_attachment(card_id: str, attachment_id: str) -> dict[str, Any]:
    """Delete an attachment from a card."""
    client = TrelloClient()
    await client.delete(f"/cards/{card_id}/attachments/{attachment_id}")
    return {"deleted": True, "attachment_id": attachment_id}
