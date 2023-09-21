from pydantic import BaseModel, validator, ValidationError, NameEmail
from typing import Optional
import datetime


def must_not_exceed_n_length(n, v):
    if len(v) > 35:
        raise ValidationError(f"Field may not exceed a length of {n}")


class PostEmployeeModel(BaseModel):
    title: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    is_off_payroll_worker: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    address_line_1: str
    city: str
    post_code: str
    address_line_2: Optional[str]
    county: Optional[str]
    country_name: Optional[str]

    # TODO add json creation https://developer.xero.com/documentation/api/payrolluk/employees POST

    @validator("title", "first_name", "last_name", "address_line_1")
    def must_not_exceed_35_chars(cls, v):
        must_not_exceed_n_length(35, v)

    @validator("city")
    def must_not_exceed_50_chars(cls, v):
        must_not_exceed_n_length(50, v)

    @validator("post_code")
    def must_not_exceed_8_chars(cls, v):
        must_not_exceed_n_length(8, v)

    @validator("gender")
    def must_be_m_or_f(cls, v):
        if v not in ["F", "M"]:
            raise ValidationError

    @validator("date_of_birth")
    def must_be_yyyy_mm_dd(cls, v):
        try:
            datetime.datetime.fromisoformat(v)
        except:
            ValidationError


class PutEmployeeModel(BaseModel):
    title: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    is_off_payroll_worker: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    address_line_1: str
    city: str
    post_code: str
    address_line_2: Optional[str]
    county: Optional[str]
    country_name: Optional[str]
    ni: Optional[str]
    # TODO add json creation https://developer.xero.com/documentation/api/payrolluk/employees PUT

    @validator("title", "first_name", "last_name", "address_line_1")
    def must_not_exceed_35_chars(cls, v):
        must_not_exceed_n_length(35, v)

    @validator("city")
    def must_not_exceed_50_chars(cls, v):
        must_not_exceed_n_length(50, v)

    @validator("post_code")
    def must_not_exceed_8_chars(cls, v):
        must_not_exceed_n_length(8, v)

    @validator("gender")
    def must_be_m_or_f(cls, v):
        if v not in ["F", "M"]:
            raise ValidationError

    @validator("date_of_birth")
    def must_be_yyyy_mm_dd(cls, v):
        try:
            datetime.datetime.fromisoformat(v)
        except:
            ValidationError
