from abc import ABC, abstractmethod
from typing import Any

class Topic():
    def __init__(self, name: str):
        self.name = name
        self.value = None

    def set_value(self, value: Any) -> None:
        self.value = value

    def get_value(self) -> Any:
        return self.value


class TopicManager():
    def __init__(self):
        self.topics = {}

    def add_topic(self, topic: Topic) -> None:
        self.topics[topic.name] = topic


class PubSub(ABC):
    def __init__(self, topic: Topic, rate: float = 0):
        self.topic = topic
        self.rate = rate
        self.data = None
        self.current_time = 0
        self.last_update_time = 0

    def tick(self, dt: float) -> bool:
        self.current_time += dt
        if (self.current_time - self.last_update_time) > self.rate:
            self.last_update_time += self.rate
            return True
        return False

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class Publisher(PubSub, ABC):
    def __init__(self, publish: Topic, rate: float = 0):
        super().__init__(publish, rate)
        
    def send(self) -> None:
        self.topic.set_value(self.data)

    def update(self, dt: float) -> None:
        if self.tick(dt):
            self.update_data()
            self.send()

    @abstractmethod
    def update_data(self) -> None:
        pass


class Subscriber(PubSub, ABC):
    def __init__(self, subscribe: Topic, rate: float = 0):
        super().__init__(subscribe, rate)
        self.processed = None

    def read(self) -> Any:
        self.data = self.topic.get_value()
        return self.data

    def update(self, dt: float) -> None:
        if self.tick(dt):
            self.read()
            self.process_data()

    def get_data(self) -> Any:
        return self.processed;
    
    @abstractmethod
    def process_data(self) -> None:
        pass
