from genie.backends.exceptions import BackendException


class CustomerAlreadyExists(BackendException):
    status = 409
    error_message = 'Customer with email already exists'
