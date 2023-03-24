from xeroapi.payroll_UK_validators import PostEmployeeModel, PutEmployeeModel


def test_post_employee_model_no_optional():
    kwargs = {
        "title": "Mr",
        "first_name": "Yoyo",
        "last_name": "Dobbins",
        "date_of_birth": "2022-07-01",
        "gender": "M",
        "address_line_1": "1 Street",
        "city": "Numenor",
        "post_code": "N190N7",
    }
    s = PostEmployeeModel(**kwargs)


def test_put_employee_model_no_optional():
    kwargs = {
        "title": "Mr",
        "first_name": "Yoyo",
        "last_name": "Dobbins",
        "date_of_birth": "2022-07-01",
        "gender": "M",
        "address_line_1": "1 Street",
        "city": "Numenor",
        "post_code": "N190N7",
    }
    s = PutEmployeeModel(**kwargs)
