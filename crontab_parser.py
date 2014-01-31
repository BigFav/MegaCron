class Command:
    def __init__(self):
        self.min = []
		self.hour = []
		self.dom = []
		self.mon = []
		self.dow = []
		self.cmd = ""
    def parseMin(self, str):
		parsed = str.split(',')
		for min in parsed:
			
		
commands = []
for f in open(test, 'r').readlines():
	tokens = filter(None, f.split(' '))
	if len(tokens != 6):
		#How do we want to proceed if 1 bad entry is found
	Command.min = Command.parseMin(tokens[0].replace('*', '0-59'))
	Command.hour = hr
	Command.dom = dom
	Command.mon = mon
	Command.dow = dow
	Command.cmd = cmd