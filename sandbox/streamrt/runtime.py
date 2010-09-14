from streamrt import NotImplementException

class Block:
	
	callbacks = list()
	
	def init(self):
		""" initializes the stateful information, and returns self """
		raise NotImplementException()
		
	def process(self, data, channel = None):
		""" processes a datagram.
		Feed the result to all callbacks, and then returns it.
		"""
		raise NotImplementException()
	
class IdentityBlock(Block):
	
	def init(self):
		return self
	
	def process(self, data):
		if self.callbacks:
			[f(data) for f in self.callbacks]
		return data

