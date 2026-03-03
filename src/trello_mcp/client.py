from typing import Any

import httpx

from trello_mcp.config import get_config
from trello_mcp.exceptions import (
    TrelloAuthError,
    TrelloError,
    TrelloNotFoundError,
    TrelloRateLimitError,
)


class TrelloClient:
    def __init__(self) -> None:
        config = get_config()
        self._base_url = config.base_url
        self._auth_params = {"key": config.api_key, "token": config.token}

    def _url(self, endpoint: str) -> str:
        return f"{self._base_url}/{endpoint.lstrip('/')}"

    def _merge_params(self, params: dict[str, Any] | None) -> dict[str, Any]:
        merged = dict(self._auth_params)
        if params:
            merged.update(params)
        return merged

    @staticmethod
    def _handle_response(resp: httpx.Response) -> Any:
        if resp.status_code == 401:
            raise TrelloAuthError(
                "Unauthorized – check TRELLO_API_KEY and TRELLO_TOKEN",
                status_code=401,
            )
        if resp.status_code == 404:
            raise TrelloNotFoundError(
                f"Resource not found: {resp.url.path}",
                status_code=404,
            )
        if resp.status_code == 429:
            raise TrelloRateLimitError(
                "Rate limited by Trello API. Try again shortly.",
                status_code=429,
            )
        if resp.status_code >= 400:
            detail = resp.text[:200] if resp.text else f"HTTP {resp.status_code}"
            raise TrelloError(
                f"Trello API error ({resp.status_code}): {detail}",
                status_code=resp.status_code,
            )
        return resp.json()

    async def get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> Any:
        async with httpx.AsyncClient(timeout=30.0) as http:
            resp = await http.get(
                self._url(endpoint), params=self._merge_params(params)
            )
            return self._handle_response(resp)

    async def post(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        async with httpx.AsyncClient(timeout=30.0) as http:
            resp = await http.post(
                self._url(endpoint),
                params=self._merge_params(params),
                json=json,
            )
            return self._handle_response(resp)

    async def put(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        async with httpx.AsyncClient(timeout=30.0) as http:
            resp = await http.put(
                self._url(endpoint),
                params=self._merge_params(params),
                json=json,
            )
            return self._handle_response(resp)

    async def post_multipart(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> Any:
        async with httpx.AsyncClient(timeout=60.0) as http:
            resp = await http.post(
                self._url(endpoint),
                params=self._merge_params(params),
                files=files,
            )
            return self._handle_response(resp)

    async def delete(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> Any:
        async with httpx.AsyncClient(timeout=30.0) as http:
            resp = await http.delete(
                self._url(endpoint), params=self._merge_params(params)
            )
            return self._handle_response(resp)
