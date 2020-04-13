#!/usr/bin/env python3

import threading

class semaphore(object):
	def __init__(self, value=0):
		self.cond = threading.Condition()
		self.value = value

	def P(self):
		with self.cond:
			self.value -= 1
			if self.value < 0:
				self.cond.wait()
			
	def V(self):
		with self.cond:
			self.value += 1
			if self.value <= 0:
				self.cond.notify()
