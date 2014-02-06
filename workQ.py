import collections
from threading import Timer

class WorkQueue:
	def __init__(self):
		self.jobQ = collections.deque() #top is left, bottom is right

	def qsize(self): #lock?
		return len(self.jobQ)

	def empty(self): #lock?
		return (len(self.jobQ) == 0)

	def append(self, item):
		return self.jobQ.append(item)

	def prepend(self, item): #needed?
		return self.jobQ.appendleft(item)

	def pop(self):
		elem = self.jobQ.popleft()
		timer = Timer(60.0, jobNotDone, [elem])
		return (elem, timer)

	def jobDone(self, timer):
		timer.cancel()
		return True

	def jobNotDone(item):
		return self.jobQ.appendleft(item)
