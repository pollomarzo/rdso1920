import threading
import time
import logging
import random
from monitor import monitor, condition, entry
from queue import Queue


class warehouse(monitor):

    def __init__(self):
        self.len = 3
        self.storage = []
        self.amountneeded = [Queue(-1)] * self.len
        self.needparts = [condition(self)] * self.len

    @entry
    def add(self, components):
        for i, amount in enumerate(components):
            self.storage[i] += amount

        for i, comp_queue in enumerate(self.amountneeded):
            # comp_queue.top() ritorna il numero di pezzi del
            # componente i necessari al primo processo arrivato
            while (comp_queue.isEmpty()):
                if (self.storage[i] >= comp_queue.top()):
                    self.needparts[i].signal()
                else:
                    break

    @entry
    def get(self, needed):
        for i, amount in enumerate(needed):
            if (amount > 0):
                self.amountneeded[i].enqueue(amount)

        for i in range(15):
            if (amount > 0):
                amount = needed[i]
                if (self.storage[i] < amount):
                    self.needparts[i].wait()
                    self.amountneeded[i].dequeue()
                    self.storage[i] -= amount


def writer(mon, components):
    mon.add(components)


def reader(mon):
    mon.get()


if __name__ == "__main__":
    order = ["w", "r"] * 5
    random.shuffle(order)
    print(f"Order: {order}")
    wr = samewr()
    threads = []
    nr = nw = 0
    for elem in order:
        if elem == "w":
            threads.append(threading.Thread(
                name=f"writer{nw}", target=writer, args=(wr,), daemon=True))
            nw += 1
        elif elem == "r":
            threads.append(threading.Thread(
                name=f"reader{nr}", target=reader, args=(wr,), daemon=True))
            nr += 1

    for t in threads:
        t.start()

    for t in threads:
        t.join()
