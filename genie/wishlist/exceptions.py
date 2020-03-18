from genie.backends.exceptions import BackendException


class WishlistAlreadyExistsForCustomer(BackendException):
    status = 409
    error_message = 'Wishlis already exists for customer'
