
class AivenApiException(Exception):
    status_code = 400
    def __init__(self, message, status_code = 400):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = None

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv