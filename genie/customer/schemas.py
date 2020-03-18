from marshmallow import fields, validate

from genie.customer.models import Customer
from genie.schema import ModelSchema


class CustomerSchema(ModelSchema):
    model_class = Customer

    id = fields.String(required=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True, validate=validate.Length(max=80))
    wishlist_id = fields.UUID(required=False)
