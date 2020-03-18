from marshmallow import fields, validate

from genie.customer.models import CustomerModel
from genie.schema import ModelSchema


class CustomerSchema(ModelSchema):
    model_class = CustomerModel

    id = fields.String(required=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True, validate=validate.Length(max=80))
    wishlist_id = fields.UUID(required=False)
