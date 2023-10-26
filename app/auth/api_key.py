from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends

import os

api_key_header = APIKeyHeader(name="x-api-key")


async def api_key_auth(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == os.environ.get("MORNING_API_KEY"):
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Access denied: invalid API key.",
        )
