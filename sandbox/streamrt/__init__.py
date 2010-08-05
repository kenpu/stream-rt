
class S:
	
	def __init__(self):
		self._data = {}
		self._binary = {}
		
	def data(self, attr, val):
		self._data[attr] = val
		return self
		
	def binary(self, attr, val):
		self._binary[attr] = val
	
	def get(self, attr):
		if attr in self._data:
			return self._data[attr]
		elif attr in self._binary:
			return self._binary[attr]
		
		raise KeyError("%s not in %s" % (attr, str(self._data.keys() + self._binary.keys())))
	
	def __str__(self):
		return "DATA=%s, BINARY={%s}" % (str(self._data), 
					 ",".join("%s: %d bytes" % (k, len(v)) for (k,v) in self._binary.items()))
	
	def serialize(self):
		raise Exception("Not implemented")
	
	def deserialize(self):
		raise Exception("Not implemented")
	
