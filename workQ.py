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

	def prepend(self, item):
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

	"""
	def jobDone(self, item):
		self.underwayJobs = [(self.underwayJobs[i] if (self.underwayJobs[i][0] != item)) \
		for i in range(len(self.underwayJobs))]

	#checks if job has been completed, decrements time, if time is done
	#adds back to queue
	def checkAck(self):
		self.underwayJobs = [(self.underwayJobs[i][0], self.underwayJobs[i][1] - 15.0) \
		for i in range(len(self.underwayJobs))]
		
		for i in range(len(self.underwayJobs)-1, -1, -1):
			if(self.underwayJobs[i][1] <= 0.0):
				self.jobQ.appendleft(self.underwayJobs.pop(i))
	"""

