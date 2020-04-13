#!/usr/bin/env python3

import threading
import time
import logging
import random
from monitor import monitor, condition, entry

class safeprint(monitor):
	def __init__(self):
		super().__init__()

	@entry
	def print(self, *args,**kwargs):
		print(*args,**kwargs)

safeprint = safeprint().print

class pcmon(monitor):
	def __init__(self, size=1):
		super().__init__()
		self.ok2write = condition(self)
		self.ok2read = condition(self)
		self.buf = []
		self.size = size

	@entry
	def put(self, val):
		if len(self.buf) >= self.size:
			self.ok2write.wait()
		self.buf.append(val)
		self.ok2read.signal()

	@entry
	def get(self):
		if len(self.buf) == 0:
		      self.ok2read.wait()
		rval = self.buf.pop(0)
		self.ok2write.signal()
		return rval

def producer(pc):
	global buf
	for _ in range(10):
		time.sleep(random.random() * 0.5)
		val = random.randint(0, 1000)
		safeprint('P',val)
		pc.put(val)

def consumer(pc):
	for _ in range(10):
		time.sleep(random.random() * 0.5)
		safeprint('\t\tC',pc.get())

if __name__ == "__main__":
	pc = pcmon(1)
	p = threading.Thread(name='producer', target=producer, args=(pc,))
	c = threading.Thread(name='consumer', target=consumer, args=(pc,))
	p.daemon=True
	c.daemon=True
	p.start()
	c.start()
	p.join()
	c.join()

