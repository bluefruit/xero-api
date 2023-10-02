import pytest
from xeroapi import XeroClient, AccountingAPI, PayrollUKAPI
import asyncio
import os
#from dotenv import load_dotenv

# load_dotenv()
ID, SECRET = os.environ["XERO_ID"], os.environ["XERO_SECRET"]
scopes = [
    "accounting.transactions",
    "accounting.transactions.read",
    "accounting.reports.read",
    "accounting.settings",
    "accounting.settings.read",
    "payroll.timesheets",
    "payroll.timesheets.read",
    "payroll.payslip",
    "payroll.payslip.read",
    "payroll.payruns",
    "payroll.payruns.read",
    "payroll.employees.read",
    "payroll.employees"
]


def auth():
    client = XeroClient(ID, SECRET, scopes)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(client.authenticate())
    return client


@pytest.fixture()
def payroll_client():
    client = auth()
    payroll_client = PayrollUKAPI(client)
    return payroll_client


@pytest.fixture()
def accounting_client():
    client = auth()
    accounting_client = AccountingAPI(client)
    return accounting_client
