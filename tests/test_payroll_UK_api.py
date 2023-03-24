import pytest
import pprint


async def get_employee_details(payroll_client, first_name, last_name):
    # Just for testing
    employees = await payroll_client.get_employees()
    employees = employees["employees"]
    employee_id = None
    for employee in employees:
        if employee["firstName"] == first_name:
            if employee["lastName"] == last_name:
                employee_id = employee["employeeID"]
    if employee_id == None:
        raise Exception(f"Employee does not exist with name {first_name} {last_name}")
    employee_details_full = await payroll_client.get_employee_by_id(employee_id)
    status_code = employee_details_full["httpStatusCode"]
    return employee_details_full["employee"], status_code


@pytest.mark.asyncio
async def test_get_employees(payroll_client):
    response = await payroll_client.get_employees()
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_get_employee_by_id(payroll_client):
    response, status_code = await get_employee_details(
        payroll_client, "Charlotte", "Danes"
    )
    assert status_code == "OK"


@pytest.mark.asyncio
async def test_post_employee(payroll_client):
    # Fails if previously been added due to Xeros Validation
    kwargs = {
        "title": "Mr.",
        "first_name": "Edgar",
        "last_name": "Allan Po",
        "date_of_birth": "1985-03-24",
        "gender": "M",
        "address_line_1": "171 Midsummer",
        "city": "Milton Keynes",
        "post_code": "MK9 1EB",
        "email": "tester@gmail.com",
        "is_off_payroll_worker": False,
        "phone_number": "0400123456",
    }
    response = await payroll_client.post_employee(**kwargs)
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_put_employee(payroll_client):
    kwargs = {
        "title": "Mr.",
        "first_name": "Edgar",
        "last_name": "Allan Potwo",
        "date_of_birth": "1985-03-24",
        "gender": "M",
        "address_line_1": "171 Midsummer",
        "city": "Milton Keynes",
        "post_code": "MK9 1EB",
        "email": "tester2@gmail.com",
        "is_off_payroll_worker": False,
        "phone_number": "0400123456",
    }
    employees = await payroll_client.get_employees()
    employee_id = "57fb1174-142f-42f1-9222-57ff6c9a0d7c"  # Will break on different test instance, replace with correct one
    response = await payroll_client.put_employee(employee_id, **kwargs)
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_post_employment(payroll_client):
    kwargs = {}
    employee, status_code = await get_employee_details(
        payroll_client, "Charlotte", "Danes"
    )
    kwargs["payroll_calendar_id"] = employee["payrollCalendarID"]
    kwargs["NI_categories"] = [{"NICategory": "A", "StartDate": "2020-05-01"}]
    kwargs["employee_number"] = employee["employeeNumber"]
    kwargs["start_date"] = employee["startDate"]
    employee_id = employee["employeeID"]
    response = await payroll_client.post_employment(employee_id, **kwargs)
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_get_payment_method(payroll_client):
    kwargs = {}
    employee, status_code = await get_employee_details(
        payroll_client, "Charlotte", "Danes"
    )
    employee_id = employee["employeeID"]
    response = await payroll_client.get_payment_method(employee_id)
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_post_payment_method(payroll_client):
    kwargs = {}
    employee, status_code = await get_employee_details(
        payroll_client, "Charlotte", "Danes"
    )
    employee_id = employee["employeeID"]
    payment_method = "Electronically"
    account_name = "Charlotte Danes"
    account_number = "45678923"
    sort_code = "123411"
    response = await payroll_client.post_payment_method(
        employee_id,
        payment_method,
        account_name=account_name,
        account_number=account_number,
        sort_code=sort_code,
    )
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_get_employee_salary_and_wages(payroll_client):
    employee, status_code = await get_employee_details(
        payroll_client, "Charlotte", "Danes"
    )
    employee_id = employee["employeeID"]
    response = await payroll_client.get_salary_and_wages(employee_id)
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_get_employee_salary_and_wages_by_salary_and_wage_id(payroll_client):
    employee, status_code = await get_employee_details(
        payroll_client, "Charlotte", "Danes"
    )
    employee_id = employee["employeeID"]
    response = await payroll_client.get_salary_and_wages(employee_id)
    # pprint.pprint(response)
    assert response["httpStatusCode"] == "OK"

    salary_and_wages_id = response["salaryAndWages"][0]["salaryAndWagesID"]
    response = await payroll_client.get_salary_and_wages_by_salary_wage_id(
        employee_id, salary_and_wages_id
    )
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_post_salary_and_wages(payroll_client):
    employee, status_code = await get_employee_details(
        payroll_client, "Charlotte", "Danes"
    )
    employee_id = employee["employeeID"]
    response = await payroll_client.get_salary_and_wages(employee_id)
    pprint.pprint(response)

    response = await payroll_client.get_earnings_rates()
    earnings_rate_ID = response["earningsRates"][0]["earningsRateID"]  # RegularEarnings

    response = await payroll_client.post_salary_and_wages(
        employee_id,
        earnings_rate_ID,
        40,
        100,
        0,
        "04-04-2023",
        30000,
        "Active",
        "Salary",
    )
    pprint.pprint(response)
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_put_salary_and_wages(payroll_client):
    pprint.pprint(await payroll_client.get_employees())
    employee, status_code = await get_employee_details(
        payroll_client, "Charlotte", "Danes"
    )
    employee_id = employee["employeeID"]
    response = await payroll_client.get_salary_and_wages(employee_id)
    pprint.pprint(response)
    assert response["httpStatusCode"] == "OK"
    earnings_rate_ID = response["salaryAndWages"][-1]["earningsRateID"]
    salary_and_wages_id = response["salaryAndWages"][-1]["salaryAndWagesID"]
    print(employee_id, earnings_rate_ID, salary_and_wages_id)
    response = await payroll_client.put_salary_and_wages(
        employee_id,
        salary_and_wages_id,
        earnings_rate_ID,
        40,
        100,
        0,
        "04-04-2023",
        40000,
        "Active",
        "Salary",
    )
    pprint.pprint(response)
    assert response["httpStatusCode"] == "OK"


@pytest.mark.asyncio
async def test_get_earnings_rates(payroll_client):
    response = await payroll_client.get_earnings_rates()
    assert response["httpStatusCode"] == "OK"
