import pytest

from trello_mcp.tools.lists import create_list, get_board_lists


@pytest.mark.asyncio
async def test_get_board_lists(httpx_mock):
    httpx_mock.add_response(
        json=[
            {"id": "l1", "name": "To Do", "closed": False, "pos": 16384},
            {"id": "l2", "name": "Done", "closed": False, "pos": 32768},
        ]
    )
    result = await get_board_lists("board1")
    assert len(result) == 2
    assert result[0]["id"] == "l1"
    assert result[0]["name"] == "To Do"
    assert result[0]["position"] == 16384
    assert result[1]["name"] == "Done"


@pytest.mark.asyncio
async def test_create_list(httpx_mock):
    httpx_mock.add_response(
        json={"id": "l3", "name": "In Progress", "closed": False, "pos": 24576}
    )
    result = await create_list("board1", "In Progress")
    assert result["id"] == "l3"
    assert result["name"] == "In Progress"
    request = httpx_mock.get_request()
    assert "idBoard=board1" in str(request.url)
