from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_pascal
from typing import Optional
from enum import Enum
import datetime


class TrackingCategory(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal)
    name: str
    option: str
   
class LineItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal)
    description: str
    quantity: int = None
    unit_amount: float = None
    item_code: Optional[str]  = None
    account_code: str = None
    line_item_id: Optional[str] = None
    tax_type: Optional[str] = None
    tax_amount: Optional[float] = None
    line_amount: Optional[float] = None
    discount_rate: Optional[float] = None
    tracking: Optional[list[TrackingCategory]] = None



class Invoice_Type(Enum):
    acc_rec = "ACCREC"
    acc_pay = "ACCPAY"

class Status(Enum):
    draft = "DRAFT"
    submitted = "SUBMITTED"
    authorised = "AUTHORISED"

class Invoice(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal)
    type: Invoice_Type
    contact: dict[str, str]
    line_items: list[LineItem]
    date_string: Optional[datetime.date]  = None
    due_date_string: Optional[datetime.date]  = None
    line_amount_types: Optional[str]  = None
    invoice_number: Optional[str]  = None
    reference: Optional[str]  = None
    branding_theme_id: Optional[str]  = None
    url: Optional[str]  = None
    currency_code: Optional[str]  = None
    currency_rate: Optional[str]  = None
    status: Status = Status.draft
    sent_to_contact: Optional[bool]  = False
    expected_payment_date: Optional[datetime.datetime]  = None
    planned_payment_date: Optional[datetime.datetime] = None

