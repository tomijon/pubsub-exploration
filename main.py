from pubsub import *
from random import random
from math import inf
from time import time

# Distances in metres
MAX_DISTANCE = 10000
MIN_DISTANCE = 50

TIME_LIMIT = 10 # seconds
PUB_RATE = 0.1 # seconds
SUB_RATE = 0.1 # seconds

class Vector():
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def length(self) -> float:
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (other == self)

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f}) -> {self.length():.2f}m"


class PositionPublisher(Publisher):
    def __init__(self, publish: Topic, rate: float = 0):
        super().__init__(publish, rate)

    def update_data(self) -> None:
        x = (random() * (MAX_DISTANCE - MIN_DISTANCE)) + MIN_DISTANCE
        y = (random() * (MAX_DISTANCE - MIN_DISTANCE)) + MIN_DISTANCE
        vector = Vector(x, y)
        self.data = vector


class PositionSubscriber(Subscriber):
    def __init__(self, subscribe: Topic, rate: float = 0):
        super().__init__(subscribe, rate)
        self.processed = Vector(inf, inf)
        self.cache_mag = inf

    def process_data(self) -> None:
        length = self.data.length()
        if length < self.cache_mag:
            self.cache_mag = length
            self.processed = self.data


if __name__ == "__main__":
    positionTopicChannel = Topic("position")
    positionPublisher = PositionPublisher(positionTopicChannel, PUB_RATE)
    positionSubscriber = PositionSubscriber(positionTopicChannel, SUB_RATE)

    start = time()
    last = start
    best = Vector(inf, inf)

    while (now := time()) - start < TIME_LIMIT:
        dt = now - last
        last = now

        positionPublisher.update(dt)
        positionSubscriber.update(dt)

        if positionSubscriber.get_data() != best:
            best = positionSubscriber.get_data()
            print(f"Best {best} found at time {now - start:.2f})")
