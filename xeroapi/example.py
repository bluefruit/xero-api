import httpx
import os
from dotenv import load_dotenv

from .xero_client import XeroClient
from .accounting_api import AccountingAPI
from .payroll_UK_api import PayrollUKAPI
from fastapi import FastAPI, HTTPException

load_dotenv()
ID, SECRET = os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"]
scopes = [
    "accounting.transactions",
    "accounting.transactions.read",
    "accounting.reports.read",
    "payroll.settings",
    "payroll.settings.read",
    "payroll.timesheets",
    "payroll.timesheets.read",
    "payroll.payslip.read",
    "payroll.payslip",
    "payroll.payruns.read",
    "payroll.payruns",
    "payroll.employees.read",
    "payroll.employees",
]

app = FastAPI()


@app.on_event("startup")
async def shutdown():
    app.client = XeroClient(ID, SECRET, scopes)
    s = await app.client.authenticate()
    app.accounting_client = AccountingAPI(app.client)
    app.payroll_client = PayrollUKAPI(app.client)


@app.on_event("shutdown")
async def shutdown():
    app.client.close()


@app.get("/")
async def read_root():
    kwargs = {
        "title": "Mr",
        "first_name": "Yoyo",
        "last_name": "Dobbins",
        "date_of_birth": "2022-07-01",
        "gender": "m",
        "address_line_1": "1 Street",
        "city": "Numenor",
        "post_code": "N190N7",
    }
    try:
        response = await app.payroll_client.post_employee(**kwargs)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))
    return response


@app.get("/invoices")
async def read_root():
    return await app.accounting_client.get_invoices()
