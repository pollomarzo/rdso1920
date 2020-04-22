import threading
import time
import logging
import random
from monitor import monitor, condition, entry

BLQ = 0
CDG = 1
BRX = 2
LGW = 3
FCO = 4
AIRPORT_CODES = [BLQ, CDG, BRX, LGW, FCO]

class airport(monitor):
    def __init__(self, MAX):
        super().__init__()
        self.MAX = MAX
        self.n = 0
        self.station = BLQ
        self.waiting_to_load = condition(self)
        self.waiting_to_leave = condition(self)
        # dizionario: a un codice di stazione corrisponde una lista di bagagli
        self.cart_items = dict([(code, []) for code in AIRPORT_CODES])
        # dizionario: a un codice di stazione corrisponde una condition variable
        self.waiting_to_unload = dict([(code, condition(self)) for code in AIRPORT_CODES])

    @entry
    def cartat(self, dstcode):
        self.station = dstcode

        if self.n < self.MAX:
            print(f"Cart waiting for loading...")
            self.waiting_to_leave.wait()  # aspetta finché non è pieno <---
            print(f"Cart loaded")
            if self.cart_items[dstcode] != []:
                print(f"Wake up {dstcode} stations")
                self.waiting_to_unload[dstcode].signal()
        elif self.station == BLQ:
            self.n = 0
            print(f"Wake up loading stations...")
            self.waiting_to_load.signal()

    @entry
    def load(self, dstcode, owner):
        if self.n == self.MAX or self.station != BLQ:
            # aspetta che si liberi un posto e che il carrello torni a loading_station
            print(f"Loading station {threading.current_thread().getName()} stopped")
            self.waiting_to_load.wait()
        self.cart_items[dstcode]
        self.n += 1
        print(
            f"Wake up other loading stations if present ({threading.current_thread().getName()})")
        self.waiting_to_load.signal()
        if self.n == self.MAX:
            print(
                f"Cart full, wake it up ({threading.current_thread().getName()})")
            self.waiting_to_leave.signal()

    @entry
    def unload(self, dstcode):
        if self.station != dstcode:
            print(
                f"Station {dstcode} stopped ({threading.current_thread().getName()})")
            self.waiting_to_unload[dstcode].wait()
        owner = self.cart_items[dstcode].pop(0)
        if self.cart_items[dstcode] != []:
            print(f"Wake up other {dstcode} stations ({threading.current_thread().getName()})")
            self.waiting_to_unload[dstcode].signal()  # passing the bâton
        return owner

def cart(mon):
    while True:
        for code in AIRPORT_CODES:
            mon.cartat(code)    # il carrello è alla postazione code

def loadingstation(mon):
    owner = 0
    while True:
        dstcode = AIRPORT_CODES[random.randint(1, len(AIRPORT_CODES) - 1)]
        # carica la valigia del viaggiatore owner diretto a dstcode
        mon.load(dstcode, owner)
        owner += 1


# C'è un processo stazione in ciascuna destinazione (tranne BLQ)
def station(mon, dstcode):
        while True:
            # scarica dal carrello la valigia dell'utente owner
            owner = mon.unload(dstcode)
            print(f"Processing {owner} luggage to {dstcode}")

if __name__ == "__main__":
    order = ["l", "s"] * 5
    random.shuffle(order)
    print(f"Order: {order}")
    mon = airport(3)
    threads = [threading.Thread(name="cart", target=cart, args=(mon,), daemon=True)]
    nr = nw = 0
    for elem in order:
        if elem == "l":
            threads.append(threading.Thread(
                name=f"loading_station{nw}", target=loadingstation, args=(mon,), daemon=True))
            nw += 1
        elif elem == "s":
            code = AIRPORT_CODES[random.randint(1, len(AIRPORT_CODES) - 1)]
            threads.append(threading.Thread(
                name=f"station{nr}", target=station, args=(mon,code), daemon=True))
            nr += 1

    for t in threads:
        t.start()
        time.sleep(3)

    for t in threads:
        t.join()
