import pytest

from trello_mcp.tools.cards import (
    archive_card,
    create_card,
    get_card,
    get_list_cards,
    move_card,
    update_card,
)

SAMPLE_CARD = {
    "id": "c1",
    "name": "My Card",
    "desc": "Card description",
    "url": "https://trello.com/c/c1",
    "closed": False,
    "idList": "list1",
    "idBoard": "board1",
    "pos": 16384,
    "due": None,
    "dueComplete": False,
    "labels": [{"id": "lb1", "name": "Bug", "color": "red"}],
}


@pytest.mark.asyncio
async def test_get_list_cards(httpx_mock):
    httpx_mock.add_response(json=[SAMPLE_CARD])
    result = await get_list_cards("list1")
    assert len(result) == 1
    assert result[0]["id"] == "c1"
    assert result[0]["name"] == "My Card"
    assert result[0]["list_id"] == "list1"
    assert result[0]["labels"][0]["name"] == "Bug"


@pytest.mark.asyncio
async def test_get_card(httpx_mock):
    httpx_mock.add_response(json=SAMPLE_CARD)
    result = await get_card("c1")
    assert result["id"] == "c1"
    assert result["description"] == "Card description"
    assert result["board_id"] == "board1"


@pytest.mark.asyncio
async def test_create_card(httpx_mock):
    httpx_mock.add_response(json=SAMPLE_CARD)
    result = await create_card("list1", "My Card", description="Card description")
    assert result["id"] == "c1"
    assert result["name"] == "My Card"
    request = httpx_mock.get_request()
    assert "name=My+Card" in str(request.url) or "name=My%20Card" in str(request.url)


@pytest.mark.asyncio
async def test_update_card(httpx_mock):
    updated = {**SAMPLE_CARD, "name": "Updated Card"}
    httpx_mock.add_response(json=updated)
    result = await update_card("c1", name="Updated Card")
    assert result["name"] == "Updated Card"


@pytest.mark.asyncio
async def test_move_card(httpx_mock):
    moved = {**SAMPLE_CARD, "idList": "list2"}
    httpx_mock.add_response(json=moved)
    result = await move_card("c1", "list2")
    assert result["list_id"] == "list2"


@pytest.mark.asyncio
async def test_archive_card(httpx_mock):
    archived = {**SAMPLE_CARD, "closed": True}
    httpx_mock.add_response(json=archived)
    result = await archive_card("c1")
    assert result["closed"] is True
