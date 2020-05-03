#!/usr/bin/env python3

import threading

def entry(fun):
	def inner(self, *args, **kwargs):
		self.enter()
		rval = fun(self, *args, **kwargs)
		self.exit()
		return rval
	return inner

class monitor(object):
	def __init__(self):
		self.urgent = []
		self.lock = threading.RLock()

	def enter(self):
		self.lock.acquire()
			
	def exit(self):
		if self.urgent:
			wakeup = self.urgent.pop()
			wakeup.set()
		else:
			self.lock.release()

class condition(object):
	def __init__(self, monitor):
		self.q = []
		self.monitor = monitor
	
	def wait(self):
		wait = threading.Event()
		self.q.append(wait)
		self.monitor.exit()
		wait.wait()

	def signal(self):
		if self.q:
			wakeup = self.q.pop(0)
			wait = threading.Event()
			self.monitor.urgent.append(wait)
			wakeup.set()
			wait.wait()

