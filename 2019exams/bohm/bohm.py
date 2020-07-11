import random
from threading import Thread
from semaphore import Semaphore

ok2 = (Semaphore(1), Semaphore(0))


def pre(n):
    ok2[n].P()


def post(n):
    ok2[1 - n].V()


def bohm(n):
    while (True):
        pre(n)
        print(n)
        post(n)


if __name__ == "__main__":
    bohm0 = Thread(target=bohm, name="bohm-0", args=(0,), daemon=True)
    bohm1 = Thread(target=bohm, name="bohm-1", args=(1,), daemon=True)
    threads = random.sample([bohm0, bohm1], 2)
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
