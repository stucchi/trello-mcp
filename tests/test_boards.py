import pytest

from trello_mcp.tools.boards import get_board, list_my_boards


@pytest.mark.asyncio
async def test_list_my_boards(httpx_mock):
    httpx_mock.add_response(
        json=[
            {
                "id": "b1",
                "name": "Board One",
                "desc": "First board",
                "url": "https://trello.com/b/b1",
                "closed": False,
            },
            {
                "id": "b2",
                "name": "Board Two",
                "desc": "",
                "url": "https://trello.com/b/b2",
                "closed": True,
            },
        ]
    )
    result = await list_my_boards()
    assert len(result) == 2
    assert result[0]["id"] == "b1"
    assert result[0]["name"] == "Board One"
    assert result[0]["description"] == "First board"
    assert result[1]["closed"] is True


@pytest.mark.asyncio
async def test_get_board(httpx_mock):
    httpx_mock.add_response(
        json={
            "id": "b1",
            "name": "My Board",
            "desc": "A great board",
            "url": "https://trello.com/b/b1",
            "closed": False,
            "dateLastActivity": "2025-01-15T10:30:00.000Z",
        }
    )
    result = await get_board("b1")
    assert result["id"] == "b1"
    assert result["name"] == "My Board"
    assert result["description"] == "A great board"
    assert result["date_last_activity"] == "2025-01-15T10:30:00.000Z"
