import logging

from aiohttp import web
from marshmallow import ValidationError

from genie.contrib.response import JSONResponse
from genie.customer.models import CustomerModel
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

        customer = schema.make_model()
        customer.update()
        return JSONResponse(status=200)

    async def get(self):
        customer_id = _get_customer_id(self.request)
        customer = CustomerModel.get(customer_id=customer_id)
        return JSONResponse(status=200, data=customer.to_dict())


class DeleteCustomerView(web.View):

    async def delete(self):
        customer_id = _get_customer_id(self.request)
        CustomerModel.delete(customer_id=customer_id)
        return JSONResponse(status=200)


class CreateCustomerView(web.View):

    async def post(self):
        data = await self.request.json()
        schema = CustomerSchema(strict=True)
        try:
            schema = schema.load(data)
        except ValidationError as e:
            logger.debug(
                f'Error validating customer create. Error {e.messages}'
            )
            return JSONResponse(
                data={'error_message': e.messages},
                status=400
            )

        customer = schema.make_model()
        customer.save()
        return JSONResponse(status=201)


class ListCustomerView(web.View):

    async def get(self):
        customers = CustomerModel.get()
        return JSONResponse(
            data=[customer.to_dict() for customer in customers],
            status=200
        )
