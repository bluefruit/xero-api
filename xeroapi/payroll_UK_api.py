from xeroapi.xero_client import XeroClient
from xeroapi.payroll_UK_validators import PostEmployeeModel, PutEmployeeModel
import pprint


class PayrollUKAPI:
    def __init__(self, xero_client: XeroClient):
        self.client = xero_client

    def _add_optional_data_to_required(self, required_dict, optional_dict):
        for key in optional_dict:
            if optional_dict[key] != None:
                required_dict[key] = optional_dict[key]
        return required_dict

    async def get_employees(self):
        """Does not provide all the employee information unfortunately, Use to get the IDs and then use
        get_employee_by_id to get the full information if needed."""
        response = await self.client.get("payroll.xro/2.0/employees")
        print(response)
        return response

    async def get_employee_by_id(self, employee_id):
        response = await self.client.get(f"payroll.xro/2.0/employees/{employee_id}")

        return response

    async def post_employee(
        self,
        *,
        title: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        gender: str,
        is_off_payroll_worker: str = None,
        email: str = None,
        phone_number: str = None,
        address_line_1: str,
        city: str,
        post_code: str,
        address_line_2: str = None,
        county: str = None,
        country_name: str = None,
    ):
        """Creates new employee with these values"""

        # Validator
        try:
            PostEmployeeModel(
                title=title,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                is_off_payroll_worker=is_off_payroll_worker,
                email=email,
                phone_number=phone_number,
                address_line_1=address_line_1,
                city=city,
                post_code=post_code,
                address_line_2=address_line_2,
                county=county,
                country_name=country_name,
            )
        except TypeError as e:
            return e

        required_employee_data = {
            "Title": title,
            "FirstName": first_name,
            "LastName": last_name,
            "DateOfBirth": date_of_birth,
            "Gender": gender,
            "Address": None,  # To be filled by address data
        }

        optional_employee_data = {
            "Email": email,
            "PhoneNumber": phone_number,
            "IsOffPayrollWorker": None,
        }

        employee = self._add_optional_data_to_required(
            required_employee_data, optional_employee_data
        )

        required_address_data = {
            "AddressLine1": address_line_1,
            "City": city,
            "PostCode": post_code,
        }
        optional_address_data = {
            "AddressLine2": address_line_2,
            "County": county,
            "CountryName": country_name,
        }

        address = self._add_optional_data_to_required(
            required_address_data, optional_address_data
        )
        employee["Address"] = address

        args = {"json": employee}
        response = await self.client.post("/payroll.xro/2.0/employees", **args)

        return response

    async def put_employee(
        self,
        employee_id: str,
        *,
        title: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        gender: str,
        is_off_payroll_worker: str = None,
        email: str = None,
        phone_number: str = None,
        address_line_1: str,
        city: str,
        post_code: str,
        address_line_2: str = None,
        county: str = None,
        country_name: str = None,
    ):
        """Updates employee with these values"""
        # Validator
        try:
            PutEmployeeModel(
                title=title,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                is_off_payroll_worker=is_off_payroll_worker,
                email=email,
                phone_number=phone_number,
                address_line_1=address_line_1,
                city=city,
                post_code=post_code,
                address_line_2=address_line_2,
                county=county,
                country_name=country_name,
            )
        except TypeError as e:
            return e
        required_employee_data = {
            "Title": title,
            "FirstName": first_name,
            "LastName": last_name,
            "DateOfBirth": date_of_birth,
            "Gender": gender,
            "Address": None,  # To be filled by address data
        }

        optional_employee_data = {
            "Email": email,
            "PhoneNumber": phone_number,
            "IsOffPayrollWorker": None,
        }

        employee = self._add_optional_data_to_required(
            required_employee_data, optional_employee_data
        )

        required_address_data = {
            "AddressLine1": address_line_1,
            "City": city,
            "PostCode": post_code,
        }
        optional_address_data = {
            "AddressLine2": address_line_2,
            "County": county,
            "CountryName": country_name,
        }

        address = self._add_optional_data_to_required(
            required_address_data, optional_address_data
        )
        employee["Address"] = address

        args = {"json": employee}

        response = await self.client.put(
            f"payroll.xro/2.0/employees/{employee_id}", **args
        )

        return response

    async def post_employment(
        self,
        employee_id: str,
        *,
        payroll_calendar_id: str,
        start_date: str,
        employee_number: int,
        NI_categories: list,
    ):
        """PayrollCalendarID can be acquired using get_employees"""
        request = {
            "StartDate": start_date,
            "PayRollCalendarID": payroll_calendar_id,
            "EmployeeNumber": employee_number,
            "NICategories": None,
        }
        categories = []
        for element in NI_categories:
            category = {}
            if len(element) > 2 or len(element) < 1:
                raise TypeError(
                    "Must have 1 or 2 elements(NICategory and Optionally StartDate)"
                )
            category["NICategory"] = element["NICategory"]
            category["StartDate"] = element["StartDate"]
            categories.append(category)
        request["NICategories"] = categories
        args = {"json": request}
        response = await self.client.post(
            f"payroll.xro/2.0/employees/{employee_id}/employment", **args
        )

        return response

    async def get_payment_method(self, employee_id):
        response = await self.client.get(
            f"payroll.xro/2.0/employees/{employee_id}/paymentMethods"
        )

        return response

    async def post_payment_method(
        self,
        employee_id,
        payment_method,
        *,
        account_name=None,
        account_number=None,
        sort_code=None,
    ):
        args = {"paymentMethod": payment_method, "bankAccounts": []}
        if payment_method not in ["Electronically", "Cheque", "Manually"]:
            raise TypeError("Not a valid payment method")
        if payment_method == "Electronically":
            if account_name == None or account_number == None or sort_code == None:
                raise ValueError(
                    "account_name, account_number and sort_code must all be filled in when payment_method is 'Electronically'"
                )
            bankAccount = {
                "accountName": account_name,
                "accountNumber": account_number,
                "sortCode": sort_code,
            }
            args["bankAccounts"].append(bankAccount)
        kwargs = {"json": args}
        response = await self.client.post(
            f"payroll.xro/2.0/employees/{employee_id}/paymentMethods", **kwargs
        )

        return response

    async def get_salary_and_wages(self, employee_id):
        """Retrieves all the salary and wages for an active employee"""
        response = await self.client.get(
            f"payroll.xro/2.0/employees/{employee_id}/salaryAndWages"
        )

        return response

    async def get_salary_and_wages_by_salary_wage_id(
        self, employee_id, salary_and_wages_id
    ):
        """Retrieves detailed information of a salary and wages record for an employee by its unique identifier

        Useful to get a specific record, albeit seems to return the same information as salary and wages so not
        sure it's that valuable since you need to call that to get the salary_and_wage_id to call this anyway
        ."""
        response = await self.client.get(
            f"payroll.xro/2.0/employees/{employee_id}/salaryAndWages/{salary_and_wages_id}"
        )

        return response

    async def post_salary_and_wages(
        self,
        employee_id,
        earnings_rate_id,
        num_units_per_week,
        rate_per_unit,
        num_units_per_day,
        effective_from,
        annual_salary,
        status,
        payment_type,
    ):
        """Adds a salary and wages record. Salary and wages are not applicable for off-payroll workers."""
        args = {
            "NumberOfUnitsPerWeek": num_units_per_week,
            "RatePerUnit": rate_per_unit,
            "NumberOfUnitsPerDay": num_units_per_day,
            "EffectiveFrom": effective_from,
            "annualSalary": annual_salary,
            "Status": status,
            "PaymentType": payment_type,
            "earningsRateID": earnings_rate_id,
        }
        kwargs = {"json": args}
        response = await self.client.post(
            f"payroll.xro/2.0/employees/{employee_id}/salaryAndWages/", **kwargs
        )

        return response

    async def put_salary_and_wages(
        self,
        employee_id,
        salary_and_wages_id,
        earnings_rate_id,
        num_units_per_week,
        rate_per_unit,
        num_units_per_day,
        effective_from,
        annual_salary,
        status,
        payment_type,
    ):
        """Updates a salary and wages record"""
        args = {
            "earningsRateID": earnings_rate_id,
            "numberOfUnitsPerWeek": num_units_per_week,
            "ratePerUnit": rate_per_unit,
            "numberOfUnitsPerDay": num_units_per_day,
            "effectiveFrom": effective_from,
            "annualSalary": annual_salary,
            "status": status,
            "PaymentType": payment_type,
        }
        kwargs = {"json": args}
        response = await self.client.put(
            f"payroll.xro/2.0/employees/{employee_id}/salaryAndWages/{salary_and_wages_id}",
            **kwargs,
        )

        return response

    async def get_earnings_rates(self):
        response = await self.client.get("payroll.xro/2.0/earningsRates")

        return response
