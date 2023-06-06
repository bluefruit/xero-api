from xeroapi.xero_client import TenantRateLimiter
from httpx import AsyncClient
import pytest
import asyncio
@pytest.mark.asyncio
async def test_rate_limiter():
    url = "https://klipfolio.bluefruit.software/"
    rl = TenantRateLimiter()
    client = AsyncClient()
    tasks = []
    for i in range(0, 90):
        tasks.append(asyncio.create_task(rl.request(client.get, url)))
    await asyncio.gather(*tasks)
    assert 0 == 1

