import random
import threading
import time

# T1 - Sistemas Operacionais - PUCRS
# Problema 2: Jantar dos Canibais
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

class ServingPlatter:
    def __init__(self, capacity):
        self.capacity = capacity
        self.portions = 0
        self.mutex = BakeryLock(N + 1)
        self.empty = threading.Event()
        self.not_empty = threading.Event()
        self.empty.set()

    def eat(self, cannibal_id):
        self.not_empty.wait()
        self.mutex.lock(cannibal_id)
        if self.portions > 0:
            self.portions -= 1
            print(f"Canibal {cannibal_id} consumiu uma porção. Restam {self.portions} porções.")
            if self.portions == 0:
                print("Travessa vazia. Acordando o cozinheiro...")
                self.empty.set()
                self.not_empty.clear()
        self.mutex.unlock(cannibal_id)

    def refill(self):
        self.empty.wait()
        self.mutex.lock(N)
        if self.portions == 0:
            self.portions = self.capacity
            print(f"Cozinheiro reabasteceu a travessa com {self.capacity} porções.")
            self.empty.clear()
            self.not_empty.set()
        self.mutex.unlock(N)

class Cannibal(threading.Thread):
    def __init__(self, id, platter):
        super().__init__()
        self.id = id
        self.platter = platter

    def run(self):
        while True:
            time.sleep(random.uniform(0.1, 1.0))
            self.platter.eat(self.id)

class Cook(threading.Thread):
    def __init__(self, platter):
        super().__init__()
        self.platter = platter

    def run(self):
        while True:
            self.platter.refill()

def main():
    global N
    N = 5 # Canibais
    M = 10 # Porções

    platter = ServingPlatter(M)
    cannibals = [Cannibal(i, platter) for i in range(N)]
    cook = Cook(platter)

    cook.start()
    for cannibal in cannibals:
        cannibal.start()

if __name__ == "__main__":
    main()