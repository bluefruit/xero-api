from xeroapi.xero_client import XeroClient
import datetime
from typing import Optional
from xeroapi.accounting_api_models import *


class AccountingAPI:
    def __init__(self, xero_client: XeroClient):
        self.client = xero_client

    async def get_connections(self):
        response = await self.client.get("connections")

        return response

    async def get_invoices(self):
        response = await self.client.get("api.xro/2.0/Invoices")

        return response

    async def get_invoice_by_id(self, invoiceID):
        response = await self.client.get(f"api.xro/2.0/Invoices/{invoiceID}")

        return response
    
    async def post_invoice(self,

                           
                           ):
        return 

    async def get_contacts(self):
        response = await self.client.get(f"api.xro/2.0/Contacts")

        return response

    async def get_contact_groups(self):
        response = await self.client.get(f"api.xro/2.0/ContactGroups")

        return response

    async def get_contacts_by_contact_group(self, contact_group_id):
        response = await self.client.get(
            f"api.xro/2.0/ContactGroups/{contact_group_id}"
        )

        return response

    async def get_monthly_balance_sheet_by_year(self, year: int):
        date = datetime.datetime(year=year, month=12, day=31)
        params = {
            "date": date,
            "timeframe": "MONTH",
            "paymentsOnly": "False",
            "periods": 11,
            "standardLayout": "true",
        }
        response = await self.client.get(
            f"api.xro/2.0/Reports/BalanceSheet", params=params
        )
        return response

    async def get_monthly_profit_and_loss_report_by_year(self, year: int):
        start_date = datetime.datetime(year=year, month=1, day=1)
        end_date = datetime.datetime(year=year, month=12, day=31)
        params = {
            "fromDate": start_date,
            "timeframe": "MONTH",
            "paymentsOnly": "False",
            "periods": 11,
            "standardLayout": "true",
        }
        if datetime.datetime.today().year != year:
            params["toDate"] = end_date  # Empty end date defaults to current month
        else:
            params["periods"] = datetime.datetime.today().month - 1
        response = await self.client.get(
            f"api.xro/2.0/Reports/ProfitAndLoss", params=params
        )
        return response

    async def get_accounts(self):
        response = await self.client.get("api.xro/2.0/Accounts")
        return response