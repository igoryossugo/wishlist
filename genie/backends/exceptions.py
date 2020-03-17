class BackendException(Exception):
    status = 500
    error_message = 'Internal Server Error'
    error_detail = {}

    def __init__(
        self,
        status=None,
        error_message=None,
        error_code=None,
        error_detail=None
    ):
        self.status = status or self.status
        self.error_message = error_message or self.error_message
        self.error_code = error_code or self._get_error_code(self.status)
        self.error_detail = self.error_detail or error_detail

    def _get_error_code(self, status):
        error_code_map = {
            400: 'bad_request',
            403: 'forbidden',
            404: 'not_found',
            409: 'conflict',
            422: 'unprocessable_entity',
            500: 'internal_server_error',
            503: 'service_unavailable'
        }

        return error_code_map.get(status, 'unknown_error')

    def as_dict(self):
        data = {
            'status': self.status,
            'error_code': self.error_code,
            'message': self.error_message,
        }
        if self.error_detail:
            data['error_detail'] = self.error_detail

        return data
