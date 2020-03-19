from marshmallow import Schema, post_load


class ModelSchema(Schema):

    @post_load
    def make_model(self, data, **kwargs):
        if not hasattr(self, 'model_class'):
            raise AttributeError('You must set a model to your schema.')

        return self.model_class(**data)
