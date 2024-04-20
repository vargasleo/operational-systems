import random
import threading

# T1 - Sistemas Operacionais - PUCRS
# Problema 1: Produtores e Consumidores
# Leonardo Schilling - 20204008

class BakeryLock:
    def __init__(self, total_threads):
        self.total_threads = total_threads
        self.choosing = [False] * total_threads
        self.ticket = [0] * total_threads

    def lock(self, i):
        self.choosing[i] = True
        self.ticket[i] = max(self.ticket) + 1
        self.choosing[i] = False

        for o in range(self.total_threads):
            while self.choosing[o]:
                pass
            while self.ticket[o] != 0 and (self.ticket[o], o) < (self.ticket[i], i):
                pass

    def unlock(self, i):
        self.ticket[i] = 0

class CircularQueue:
    def __init__(self, size, total_threads):
        self.queue = [None] * size
        self.size = size
        self.start = 0
        self.end = 0
        self.count = 0
        self.lock = BakeryLock(total_threads)
        self.not_full = threading.Event()
        self.not_empty = threading.Event()
        self.not_full.set()
        self.not_empty.clear()

    def enqueue(self, item, thread_id):
        while True:
            self.lock.lock(thread_id)
            if self.count == self.size:
                self.lock.unlock(thread_id)
                self.not_full.clear()
                self.not_full.wait()
            else:
                break

        self.queue[self.end] = item
        self.end = (self.end + 1) % self.size
        self.count += 1
        print(f"Produtor {thread_id} produziu: {item}. Total na fila: {self.count}")
        self.lock.unlock(thread_id)
        self.not_empty.set()

    def dequeue(self, thread_id):
        while True:
            self.lock.lock(thread_id)
            if self.count == 0:
                self.lock.unlock(thread_id)
                self.not_empty.clear()
                self.not_empty.wait()
            else:
                break

        item = self.queue[self.start]
        self.start = (self.start + 1) % self.size
        self.count -= 1
        print(f"Consumidor {thread_id} consumiu: {item}. Total na fila: {self.count}")
        self.lock.unlock(thread_id)
        self.not_full.set()

class Producer(threading.Thread):
    def __init__(self, queue, producer_id):
        super().__init__()
        self.queue = queue
        self.producer_id = producer_id

    def run(self):
        while True:
            item = random.randint(1, 100)
            self.queue.enqueue(item, self.producer_id)

class Consumer(threading.Thread):
    def __init__(self, queue, consumer_id):
        super().__init__()
        self.queue = queue
        self.consumer_id = consumer_id

    def run(self):
        while True:
            self.queue.dequeue(self.consumer_id)

def main():
    queue_size = 2
    num_producers = 5
    num_consumers = 5
    total_threads = num_producers + num_consumers

    circular_queue = CircularQueue(queue_size, total_threads)

    producers = [Producer(circular_queue, i) for i in range(num_producers)]
    consumers = [Consumer(circular_queue, num_producers + i) for i in range(num_consumers)]

    for producer in producers:
        producer.start()
    for consumer in consumers:
        consumer.start()

if __name__ == "__main__":
    main()