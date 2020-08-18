

class BaseError(Exception):
    """
    base error structure class
    """
    def __init__(self, val, message):
        """
        @param val: actual value
        @param message: message shown to the user
        """
        self.val = val
        self.message = message
        super().__init__()

    def __str__(self):
        return "{} --> {}".format(self.val, self.message)


class LanguageNotSupportedException(BaseError):
    """
    exception thrown if the user uses a language that is not supported by the deep_translator
    """
    def __init__(self, val, message="There is no support for the chosen language"):
        super().__init__(val, message)


class NotValidPayload(BaseError):
    """
    exception thrown if the user enters an invalid payload
    """
    def __init__(self,
                 val,
                 message='text must be a valid text with maximum 5000 character, otherwise it cannot be translated'):
        super(NotValidPayload, self).__init__(val, message)


class TranslationNotFound(BaseError):
    """
    exception thrown if no translation was found for the text provided by the user
    """
    def __init__(self,
                 val,
                 message='No translation was found using the current translator. Try another translator?'):
        super(TranslationNotFound, self).__init__(val, message)


class ElementNotFoundInGetRequest(BaseError):
    """
    exception thrown if the html element was not found in the body parsed by beautifulsoup
    """
    def __init__(self,
                 val,
                 message='Required element was not found in the API response'):
        super(ElementNotFoundInGetRequest, self).__init__(val, message)


class NotValidLength(BaseError):
    """
    exception thrown if the provided text exceed the length limit of the translator
    """
    def __init__(self, val, min_chars, max_chars):
        message = "Text length need to be between {} and {} characters".format(min_chars, max_chars)
        super(NotValidLength, self).__init__(val, message)


class RequestError(Exception):
    """
    exception thrown if an error occured during the request call, e.g a connection problem.
    """
    def __init__(self, message="Request exception can happen due to an api connection error. "
                               "Please check your connection and try again"):
        self.message = message

    def __str__(self):
        return self.message
