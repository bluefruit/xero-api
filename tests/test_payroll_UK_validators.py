from xeroapi.payroll_UK_validators import PostEmployeeModel, PutEmployeeModel


def test_post_employee_model_no_optional():
    payload = {
        "Title": "Mr",
        "FirstName": "Yoyo",
        "LastName": "Dobbins",
        "DateOfBirth": "2022-07-01",
        "Gender": "M",
        "AddressLine1": "1 Street",
        "City": "Numenor",
        "PostCode": "N190N7"
    }
    s = PostEmployeeModel(**payload)


def test_put_employee_model_no_optional():
    payload = {
        "Title": "Mr",
        "FirstName": "Yoyo",
        "LastName": "Dobbins",
        "DateOfBirth": "2022-07-01",
        "Gender": "M",
        "AddressLine1": "1 Street",
        "City": "Numenor",
        "PostCode": "N190N7"
    }
    s = PutEmployeeModel(**payload)
