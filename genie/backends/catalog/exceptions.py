from genie.backends.exceptions import BackendException


class ItemNotFound(BackendException):
    status = 404
    error_message = 'Item not found'
