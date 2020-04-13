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


class samewr(monitor):
    def __init__(self):
        super().__init__()
        self.same_number = condition(self)
        self.buf = Queue(-1)
        self.n_r = 0
        self.n_w = 0

    @entry
    def put(self, val):
        self.n_w += 1
        print(f"{threading.current_thread().getName()} writes", val)
        self.buf.put(val)
        if (self.n_r != self.n_w):
            self.same_number.wait()

        self.same_number.signal()
        self.n_w -= 1

    @entry
    def get(self):
        self.n_r += 1
        if (self.n_w != self.n_r):
            self.same_number.wait()
        else:
            self.same_number.signal()
        val = self.buf.get()
        print(f"{threading.current_thread().getName()} reads", val)
        self.same_number.signal()
        self.n_r -= 1
        return val


def writer(wr):
    time.sleep(1)
    val = random.randint(0, 1000)
    wr.put(val)


def reader(wr):
    time.sleep(1)
    wr.get()

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
