import os

from common import SingletonMeta


class Configs(metaclass = SingletonMeta):
    def __init__(self):
        self.kwargs = {}

    def run_tasks(self, **kwargs) -> "Configs":
        self.kwargs['ENV'] = os.environ.get('ENV')
        self.kwargs['TERMINAL_CODE_SANDBOX'] = os.environ.get('TERMINAL_CODE_SANDBOX')
        self.kwargs['TERMINAL_CODE_PRODUCTION'] = os.environ.get('TERMINAL_CODE_PRODUCTION')
        self.kwargs['SECRET_KEY_SANDBOX'] = os.environ.get('SECRET_KEY_SANDBOX')
        self.kwargs['SECRET_KEY_PRODUCTION'] = os.environ.get('SECRET_KEY_PRODUCTION')
        self.kwargs['PAYMENT_RETURN'] = os.environ.get('PAYMENT_RETURN')

        return self

    def get_config(self, name_config: str) -> str:
        return self.kwargs.get(name_config, None)



def get_config() -> Configs:
    return Configs().run_tasks()