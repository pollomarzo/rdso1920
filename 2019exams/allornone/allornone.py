import threading
import time
import logging
import random
from monitor import monitor, condition, entry
from queue import Queue


class allornone(monitor):
    def __init__(self):
        super().__init__()
        self.ok2read = condition(self)
        self.waitingReaders = 0
        self.buffer = []

    @entry
    def put(self, val):
        self.buffer.append(val)
        print(f"{threading.current_thread().getName()} puts {val}")
        if self.waitingReaders > 0:
            print(f"{threading.current_thread().getName()} wakes up readers")
            self.ok2read.signal()
        print(f"{threading.current_thread().getName()} exits")

    @entry
    def get(self):
        print(f"{threading.current_thread().getName()} enters get");
        if self.buffer == []:
            self.waitingReaders += 1
            print(f"{threading.current_thread().getName()} blocks")
            self.ok2read.wait()
            print(f"{threading.current_thread().getName()} wakes up")
            self.waitingReaders -= 1
        val = self.buffer[0]
        print(f"{threading.current_thread().getName()} gets {val}")
        if self.waitingReaders == 0:
            print(f"{threading.current_thread().getName()} is last")
            self.buffer.pop(0)
        else:
            print(f"{threading.current_thread().getName()} wakes up its friends")
            self.ok2read.signal()
        
        print(f"{threading.current_thread().getName()} exits")
        return val


def writer(wr,nw):
    time.sleep(1)
    wr.put(nw)


def reader(wr):
    time.sleep(1)
    wr.get()


if __name__ == "__main__":
    order = ["w", "r"] * 5
    random.shuffle(order)
    # order = ['w', 'r', 'r', 'w', 'w', 'w', 'w', 'r', 'r', 'r']
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
