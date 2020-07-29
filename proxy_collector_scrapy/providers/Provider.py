from abc import abstractmethod


class Provider:
    @abstractmethod
    def get_requests(self):
        pass

    @abstractmethod
    def get_proxies(self, response):
        pass

    @abstractmethod
    def get_next(self, response):
        pass
