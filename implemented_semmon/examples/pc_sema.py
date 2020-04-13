#!/usr/bin/env python3

import threading
import time
import random
from semaphore import semaphore

buf = []
full = semaphore(0)
empty = semaphore(1)

#print is not atomic ;-)
mutex = semaphore(1)
def safeprint(*args,**kwargs):
	mutex.P()
	print(*args,**kwargs)
	mutex.V()

def producer():
	for _ in range(20):
		time.sleep(random.random() * 0.5)
		val = random.randint(0, 1000)
		safeprint('P', val)
		empty.P()
		buf.append(val)
		full.V()
		
def consumer():
	for _ in range(20):
		time.sleep(random.random() * 0.5)
		full.P()
		val = buf.pop(0)
		empty.V()
		safeprint('\t\tC', val)

if __name__ == "__main__":
	p = threading.Thread(name='producer', target=producer)
	c = threading.Thread(name='consumer', target=consumer)
	p.daemon = c.daemon = 1
	p.start()
	c.start()
	p.join()
	c.join()



