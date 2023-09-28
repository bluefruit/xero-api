from xeroapi.xero_client import TenantRateLimiter
from httpx import AsyncClient
import pytest
import asyncio
from time import time
@pytest.mark.asyncio
async def test_rate_limiter():
    url = "https://klipfolio.bluefruit.software/"
    rl = TenantRateLimiter()
    client = AsyncClient()
    tasks = []
    start_time = time()
    for i in range(0, 90):
        tasks.append(asyncio.create_task(rl.request(client.get, url)))
    await asyncio.gather(*tasks)
    end_time = time()
    # Rate limit is 60 a second in a rolling window so 90 requests should take a minimum of
    # 60 seconds. 
    assert end_time >= start_time + 60
    assert end_time <= start_time + 70

