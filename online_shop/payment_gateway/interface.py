from abc import ABC, abstractmethod


class BaseGateway(ABC):

    @abstractmethod
    def request(self, payment):
        ...

    @abstractmethod
    def verify(self, payment):
        ...