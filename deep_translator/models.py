from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    def __init__(self):
        super(BaseTranslator, self).__init__()

    @abstractmethod
    def _validate_payload(self, payload):
        pass

    @abstractmethod
    def translate(self, payload):
        pass



