from __future__ import annotations
from abc import ABC, abstractmethod


class Subject(ABC):

    """
    
    Sujeto observado
    
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class Observer(ABC):

    """
    
    Observer

    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass