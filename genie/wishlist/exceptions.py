from genie.backends.exceptions import BackendException


class WishlistAlreadyExistsForCustomer(BackendException):
    status = 409
    error_message = 'Wishlis already exists for customer'


class CustomerNotSet(BackendException):
    status = 403
    error_message = 'Customer must be set to save wishlist'
