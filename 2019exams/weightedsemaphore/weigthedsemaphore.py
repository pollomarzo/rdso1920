import threading
import time
import logging
import random
from monitor import monitor, condition, entry

class wsem(monitor):
    def __init__(self, initial_weight):
        super().__init__()
        # invariant: sum(P(w)) - sum(V(w)) >= initial_weight
        self.weight = initial_weight
        self.inside_weights = []
        self.invariant = condition(self)

    @entry
    def P(self, w):
        self.inside_weights.append(w)
        if self.weight - w < 0:
            print(f"{threading.current_thread().getName()} blocked entering")
            self.invariant.wait()

        self.weight -= self.inside_weights.pop(0)
        if self.inside_weights != [] and self.weight - self.inside_weights[0] >= 0:
            self.invariant.signal()
        else:
            print(f"{threading.current_thread().getName()} did not pass baton")

    @entry
    def V(self, w):
        self.weight += w
        if self.inside_weights != [] and self.weight - self.inside_weights[0] >= 0:
            self.invariant.signal()
        else:
            print(f"{threading.current_thread().getName()} did not pass baton")


def process(mon, weight):
    wp, wv = weight
    print(f"{threading.current_thread().getName()} does P")
    mon.P(wp)
    time.sleep(random.randint(1, 3))
    print(f"{threading.current_thread().getName()} leaving")
    mon.V(wv)
    print(f"{threading.current_thread().getName()} done V")

if __name__ == "__main__":
    weights = [(random.randint(1, 3), random.randint(1, 3)) for _ in range(10)]
    print(f"Weights: {weights}")
    wsem_mon = wsem(4)
    threads = []
    for index, weight in enumerate(weights):
        threads.append(threading.Thread(
            name=f"process{index}", target=process, args=(wsem_mon, weight), daemon=True))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
