from pydantic import BaseModel, field_validator, ValidationError, NameEmail, ConfigDict
from pydantic.alias_generators import to_pascal
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
    is_off_payroll_worker: Optional[bool] = False
    email: Optional[str] = ""
    phone_number: Optional[str] = ""
    address_line_1: str
    city: str
    post_code: str
    address_line_2: Optional[str] = ""
    county: Optional[str] = ""
    country_name: Optional[str] = "United Kingdom"

    @field_validator("title", "first_name", "last_name", "address_line_1")
    def must_not_exceed_35_chars(cls, v):
        must_not_exceed_n_length(35, v)

    @field_validator("city")
    def must_not_exceed_50_chars(cls, v):
        must_not_exceed_n_length(50, v)

    @field_validator("post_code")
    def must_not_exceed_8_chars(cls, v):
        must_not_exceed_n_length(8, v)

    @field_validator("gender")
    def must_be_m_or_f(cls, v):
        if v not in ["F", "M"]:
            raise ValidationError

    @field_validator("date_of_birth")
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
    is_off_payroll_worker: Optional[bool] = False
    email: Optional[str] = ""
    phone_number: Optional[str] = ""
    address_line_1: str
    city: str
    post_code: str
    address_line_2: Optional[str] = ""
    county: Optional[str] = ""
    country_name: Optional[str] = "United Kingdom"
    ni: Optional[str] = ""

    @field_validator("title", "first_name", "last_name", "address_line_1")
    def must_not_exceed_35_chars(cls, v):
        must_not_exceed_n_length(35, v)

    @field_validator("city")
    def must_not_exceed_50_chars(cls, v):
        must_not_exceed_n_length(50, v)

    @field_validator("post_code")
    def must_not_exceed_8_chars(cls, v):
        must_not_exceed_n_length(8, v)

    @field_validator("gender")
    def must_be_m_or_f(cls, v):
        if v not in ["F", "M"]:
            raise ValidationError

    @field_validator("date_of_birth")
    def must_be_yyyy_mm_dd(cls, v):
        try:
            datetime.datetime.fromisoformat(v)
        except:
            ValidationError
