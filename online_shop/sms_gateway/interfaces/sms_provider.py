from abc import ABC, abstractmethod



class BaseSMSProvider(ABC):

    @abstractmethod
    def send(self, *, data: dict) -> bool:
        pass

   