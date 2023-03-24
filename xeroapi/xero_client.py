import httpx
import asyncio
from xeroapi.tokens import get_access_token
import datetime
import pprint


class TenantRateLimiter:
    def __init__(self):
        """
        Per Tenant:
            5 Concurrent Calls at any one time
            60 calls per minute, Rolling 60 second window
            5000 calls per day, Probably a rolling day window
        All Tenants:
            10000 calls per minute
        """
        self.active_calls = 0
        self.calls_this_minute = 0
        self.calls_this_day = 0

    async def request(self, request, *args, **kwargs):
        """If there are too many requests this could end up choking on dealing with too many requests
        However, It should allow temporary bursts at full speed, then drop down to average throughput if it keeps
        getting hammered."""
        if self.calls_this_day < 5000:
            self.calls_this_day += 1
            if self.calls_this_minute < 60:
                self.calls_this_minute += 1
                if self.active_calls < 5:
                    self.active_calls += 1
                    response = await request(*args, **kwargs)
                    self.active_calls -= 1
                else:
                    asyncio.sleep(
                        0.3
                    )  # 5 per second so average throughput is one per 0.2 seconds
                    self.request(request, *args, *kwargs)
                self.calls_this_minute -= 1
            else:
                asyncio.sleep(
                    1.5
                )  # 60 per minute so average throughput is one per second
                self.request(request, *args, *kwargs)
            self.calls_this_day -= 1
        else:
            asyncio.sleep(25)  # 5000 a day so average throughput is 1 per 17.28 Seconds
            self.request(request, *args, *kwargs)
        return response


class XeroClient:
    def __init__(self, id, secret, scopes):
        """Important. Each method must only do one request or the rate limiter won't work.
        This class is intended to act as a simpler fully async Xero API not as the main program.

        Xero also creates it's own Python Xero API it's just not very good and not fully async."""
        self.client = httpx.AsyncClient(base_url="https://api.xero.com/")
        self.rate_limiter = TenantRateLimiter()
        self.token = None
        self.id = id
        self.secret = secret
        self.scopes = scopes

    async def close(self):
        await self.client.aclose()

    async def rate_limit(self, func, *args, **kwargs):
        response = await self.rate_limiter.request(func, *args, **kwargs)
        return response

    async def check_authentication(self):
        if self.token != None:
            current_time = datetime.datetime.today()
            if current_time > self.token.expires_at:
                await self.authenticate()

    async def authenticate(self):
        token = await get_access_token(self.client, self.id, self.secret, self.scopes)
        self.token = token
        await self.client.aclose()  # Since we want a default header containing the access token
        # We recreate the client everytime we reauthenticate
        headers = {
            "Authorization": f"Bearer {token.access_token}",
            "Accept": "application/json",
        }
        self.client = httpx.AsyncClient(
            base_url="https://api.xero.com/", headers=headers
        )

    def status_check(func):
        async def kernel(*args, **kwargs):
            result = await func(*args, **kwargs)
            try:
                result.raise_for_status()
            except Exception as e:
                raise Exception(f"{result.status_code}: {pprint.pformat(result.json())}")
            return result.json()
        return kernel

    @status_check
    async def get(self, *args, **kwargs):
        await self.check_authentication()
        response = await self.rate_limit(self.client.get, *args, **kwargs)
        return response

    @status_check
    async def post(self, *args, **kwargs):
        await self.check_authentication()
        response = await self.rate_limit(self.client.post, *args, **kwargs)
        return response

    @status_check
    async def put(self, *args, **kwargs):
        await self.check_authentication()
        response = await self.rate_limit(self.client.put, *args, **kwargs)
        return response
