In order to run example.py use
poetry run uvicorn xero-api.example:app --reload

# Example code
    import asyncio

    client = XeroClient(ID, SECRET, scopes)
    s = asyncio.run(await client.authenticate()) # asyncio.run() only required for the example. If using an async event loop already
    e.g fastapi then it's not needed.
    accounting_client = AccountingAPI(client)