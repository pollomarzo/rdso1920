import threading
import time
import logging
import random
from monitor import monitor, condition, entry
from queue import Queue


class safeprint(monitor):
    def __init__(self):
        super().__init__()

    @entry
    def print(self, *args, **kwargs):
        print(*args, **kwargs)


safeprint = safeprint().print


class allornone(monitor):
    def __init__(self):
        super().__init__()
        self.readers = condition(self)
        self.writers = condition(self)
        self.data = None
        self.nr = 0

    @entry
    def put(self, val):
        print(f"{threading.current_thread().getName()} enter put")
        if self.data != None:
            self.writers.wait()
        self.data = val
        print(f"{threading.current_thread().getName()} wrote {val}")
        if self.nr == 0:
            self.writers.wait()
        print(f"{threading.current_thread().getName()} exit")
        self.readers.signal()
        self.data = None
        self.writers.signal()
        print(f"{threading.current_thread().getName()} exit put")

    @entry
    def get(self):
        print(f"{threading.current_thread().getName()} enter get");
        self.nr += 1
        if self.data == None:
            self.readers.wait()
        val = self.data
        print(f"{threading.current_thread().getName()} read {val}")
        if self.nr == 1:
            self.writers.signal()
        else:
            self.readers.signal()
        self.nr -= 1
        print(f"{threading.current_thread().getName()} exit get")
        return val


def writer(wr,nw):
    time.sleep(1)
    wr.put(nw)


def reader(wr):
    time.sleep(1)
    wr.get()


if __name__ == "__main__":
    # order = ["w", "r"] * 5
    # random.shuffle(order)
    order = ['w', 'r', 'r', 'w', 'w', 'w', 'w', 'r', 'r', 'r']
    print(f"Order: {order}")
    wr = allornone()
    threads = []
    nr = nw = 0
    for elem in order:
        if elem == "w":
            threads.append(threading.Thread(
                name=f"writer{nw}", target=writer, args=(wr,nw), daemon=True))
            nw += 1
        elif elem == "r":
            threads.append(threading.Thread(
                name=f"reader{nr}", target=reader, args=(wr,), daemon=True))
            nr += 1

    for t in threads:
        t.start()
        time.sleep(3)

    for t in threads:
        t.join()
