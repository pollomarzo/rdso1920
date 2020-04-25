# NOTE: Questa versione in python non risolve effettivamente l'esercizio in quanto blocca
# tutti i processi che decidono di entrare non appena uno dei processi già all'interno
# decide di uscire

import threading
import time
import logging
import random
from semaphore import semaphore
from queue import Queue

class SAU:
    def __init__(self):
        super().__init__()
        self.readytoleave = []
        self.n = 0
        self.blocked = []
        self.open = True
        self.mutex = semaphore(1)

    def enter(self):
        self.mutex.P()
        if not self.open:
            block_sem = semaphore(0)
            self.blocked.append(block_sem)
            print(f"{threading.current_thread().getName()} stuck while entering")
            self.mutex.V()
            block_sem.P()
            if self.blocked != []:
                self.blocked.pop(0).V()
        # Entra nella sezione e salva il processo
        self.n += 1
        self.mutex.V()

    def exit(self):
        self.mutex.P()
        self.n -= 1

        if self.n != 0:
            inside_sem = semaphore(0)
            self.readytoleave.append(inside_sem)
            if self.open:
                self.open = False
            self.mutex.V()
            inside_sem.P()

        if self.readytoleave == []:
            print(
                f"Last process exit {threading.current_thread().getName()}")
            self.open = True
            if self.blocked != []:
                print(f"Last process exit {threading.current_thread().getName()}")
                self.blocked.pop(0).V()
            else:
                self.mutex.V()
        else:
            self.readytoleave.pop(0).V()


def process(sau):
    time.sleep(random.randint(1, 10))
    sau.enter()
    print(f"{threading.current_thread().getName()} enter SAU")
    time.sleep(random.randint(1, 3))
    print(f"{threading.current_thread().getName()} trying to exit")
    sau.exit()
    print(f"{threading.current_thread().getName()} exited SAU")


if __name__ == "__main__":
    sau = SAU()
    threads = []
    for index in range(10):
        threads.append(threading.Thread(
            name=f"process{index}", target=process, args=(sau,), daemon=True))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
