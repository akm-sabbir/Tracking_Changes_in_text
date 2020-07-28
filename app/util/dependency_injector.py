from typing import Type

from injector import Injector, T


class DependencyInjector:
    __injector = Injector()

    @classmethod
    def get_instance(cls, class_name: Type[T]):
        return cls.__injector.get(class_name)
