from marshmallow import fields, Schema


class WishlistSchema(Schema):
    customer_id = fields.UUID(required=True)
