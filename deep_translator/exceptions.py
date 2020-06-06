
class BaseError(Exception):
    def __init__(self, val, message):
        self.val = val
        self.message = message
        super().__init__()

    def __str__(self):
        return "{} --> {}".format(self.val, self.message)


class LanguageNotSupportedException(BaseError):
    def __init__(self, val, message="There is no support for the chosen language"):
        super().__init__(val, message)


class NotValidPayload(BaseError):
    def __init__(self,
                 val,
                 message='payload must be a valid text with maximum 5000 character, otherwise it cannot be translated'):
        super(NotValidPayload, self).__init__(val, message)


class ElementNotFoundInGetRequest(BaseError):
    def __init__(self,
                 val,
                 message='Element was not found in the get request.'):
        super(ElementNotFoundInGetRequest, self).__init__(val, message)


class NotValidLength(BaseError):
    def __init__(self, val, message="Length of payload need to be between 0 and 5000"):
        super(NotValidLength, self).__init__(val, message)
