from xeroapi.accounting_api_models import *

def test_invoice_model():
    payload = r"""{
            "Type": "ACCREC",
            "Contact": {
                "ContactID": "eaa28f49-6028-4b6e-bb12-d8f6278073fc"
            },
            "Date": "\/Date(1518685950940+0000)\/",
            "DueDate": "\/Date(1518685950940+0000)\/",
            "DateString": "2009-05-27T00:00:00",
            "DueDateString": "2009-06-06T00:00:00",
            "LineAmountTypes": "Exclusive",
            "LineItems": [
                {
                "Description": "Consulting services as agreed (20% off standard rate)",
                "Quantity": "10",
                "UnitAmount": "100.00",
                "AccountCode": "200",
                "DiscountRate": "20"
                }
            ]
    }"""
    Invoice.model_validate_json(payload)


def test_invoice_model_2():
    payload = r"""{
  "Type": "ACCREC",
  "CurrencyCode": "USD",
  "Contact": {
    "ContactID": "eaa28f49-6028-4b6e-bb12-d8f6278073fc"
  },
  "Date": "\/Date(1518685950940+0000)\/",
  "DueDate": "\/Date(1518685950940+0000)\/",
  "DateString": "2009-05-27T00:00:00",
  "DueDateString": "2009-06-06T00:00:00",
  "LineAmountTypes": "Inclusive",
  "LineItems": [
    {
      "Description": "Consulting services as agreed",
      "Quantity": "5.0000",
      "UnitAmount": "99",
      "AccountCode": "200",
      "Tracking": [
        {
          "Name": "Activity/Workstream",
          "Option": "Onsite consultancy"
        }
      ]
    }
  ]
}
"""
    x = Invoice.model_validate_json(payload)
