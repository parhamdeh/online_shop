from abc import ABC, abstractmethod



class BaseSMSProvider(ABC):

    @abstractmethod
    def send(self, *, phone: str, message: str) -> bool:
        pass

    @abstractmethod
    def send_verify_code(self, *, phone: str, code: str) -> bool:
        pass

   