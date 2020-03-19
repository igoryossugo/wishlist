import logging

from aiohttp import web
from marshmallow import ValidationError

from genie.contrib.response import JSONResponse
from genie.customer.models import Customer, CustomerModel
from genie.customer.schemas import CustomerSchema

logger = logging.getLogger(__name__)


def _get_customer_id(request):
    return request.match_info['customer_id']


class GetOrUpdateCustomerView(web.View):

    async def put(self):
        customer_id = _get_customer_id(self.request)
        data = await self.request.json()
        data['id'] = customer_id

        schema = CustomerSchema(strict=True)
        try:
            schema = schema.load(data)
        except ValidationError as e:
            logger.debug(
                f'Error validating customer update. Error {e.messages}'
            )
            return JSONResponse(
                data={'error_message': e.messages},
                status=400
            )

        customer_model = schema.make_model()
        customer = Customer(id=customer_model.id)
        customer.update(customer)
        return JSONResponse(status=200, data=customer.to_dict())

    async def get(self):
        customer_id = _get_customer_id(self.request)
        customer = CustomerModel(id=customer_id).get()
        return JSONResponse(status=200, data=customer.to_dict())


class DeleteCustomerView(web.View):

    async def delete(self):
        customer_id = _get_customer_id(self.request)
        Customer(id=customer_id).delete()
        return JSONResponse(status=200)


class CreateCustomerView(web.View):

    async def post(self):
        data = await self.request.json()
        try:
            customer = CustomerSchema().load(data)
        except ValidationError as e:
            logger.debug(
                f'Error validating customer create. Error {e.messages}'
            )
            return JSONResponse(
                data={'error_message': e.messages},
                status=400
            )

        customer = Customer.create(name=customer.name, email=customer.email)
        customer.save()
        return JSONResponse(status=201)


class ListCustomerView(web.View):

    async def get(self):
        customers = CustomerModel.list()
        return JSONResponse(
            data=[customer.to_dict() for customer in customers],
            status=200
        )
