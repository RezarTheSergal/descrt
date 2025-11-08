import random


class BitGenerator:
    @staticmethod
    def generate(length):
        return ''.join(random.choice('01') for _ in range(length))
