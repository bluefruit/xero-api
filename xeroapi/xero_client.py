import httpx
import asyncio
from xeroapi.tokens import get_access_token
import datetime
from collections import deque


class RateLimitException(Exception):
    pass

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
        self.minute_requests = deque()
        self.day_requests = deque()

    async def request(self, request, *args, **kwargs):
        bool, wait = self.check_limits()
        while(not bool):
            await asyncio.sleep(wait)
            bool, wait = self.check_limits()
        print(datetime.datetime.now())
        self.active_calls += 1
        time = datetime.datetime.now()
        self.minute_requests.append(time)
        self.day_requests.append(time)
        try:
            s = await request(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            #raise RateLimitException(f"Rate Limit Error, \n{s.headers}\n{e}\n")
            s = await self.request(request, *args, **kwargs)
            self.active_calls -= 1
            return s
        self.active_calls -= 1
        return s
    
    def check_limits(self):
        print(len(self.minute_requests), len(self.day_requests), self.active_calls)
        if(self.active_calls >= 5):
            time_to_wait = 0.05
            state = False
        elif(self.minute_check() == False):
            time_to_wait = 1
            state = False
        elif(self.day_check() == False):
            time_to_wait = 17.28
            state = False
        else:
            state = True
        if(state == False):
            return False, time_to_wait
        return state, 0
    
    def minute_check(self):
        ctime = datetime.datetime.now()
        ctime = ctime - datetime.timedelta(seconds=60)
        count = 0
        for time in self.minute_requests:
            if(time < ctime):
                count += 1
        for i in range(0, count):
            self.minute_requests.popleft()
        size = len(self.minute_requests)
        if(size >= 60):
            return False
        else:
            return True
        
    def day_check(self):
        ctime = datetime.datetime.now()
        ctime = ctime - datetime.timedelta(days=1)
        count = 0
        for time in self.day_requests:
            if(time < ctime):
                count += 1
        for i in range(0, count):
            self.day_requests.popleft()
        size = len(self.day_requests)
        if(size >= 5000):
            return False
        else:
            return True


class XeroClient:
    def __init__(self, id, secret, scopes):
        """Important. Each method must only do one request or the rate limiter won't work.
        This class is intended to act as a simpler fully async Xero API not as the main program.

        Xero also creates it's own Python Xero API it's just not very good and not fully async."""
        self.client = httpx.AsyncClient(base_url="https://api.xero.com/", timeout =10.0)
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
            base_url="https://api.xero.com/", headers=headers, timeout =10.0
        )

    def status_check(func):
        async def kernel(*args, **kwargs):
            result = await func(*args, **kwargs)
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
