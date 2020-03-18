from aiohttp import web

from genie.customer import views


def build_urls(prefix=''):
    return [
        web.view(
            f'{prefix}/',
            views.ListCustomerView
        ),
        web.view(
            f'{prefix}/register/',
            views.CreateCustomerView
        ),
        web.view(
            f'{prefix}/'
            r'{customer_id:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}}/',  # noqa
            views.GetOrUpdateCustomerView
        ),
        web.view(
            f'{prefix}/'
            r'{customer_id:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}}/',  # noqa
            'delete/',
            views.DeleteCustomerView
        ),
    ]
