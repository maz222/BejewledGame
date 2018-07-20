class Singleton:
	def __init__(self, decorated):
		self._decorated = decorated
	def instance(self):
		try:
			return self._instance
		except AttributeError:
			self._instance = self._decorated()
			return self._instance
	def __call__(self):
		raise TypeError("Singletons must be acessed through .instance()")
	def __instancecheck__(self, inst):
		return isinstance(inst, self._decorated)

@Singleton
class GameConstants:
		def __init__(self):
			self.data = {}
			self.data["gridSize"] = 5
		def get(self, dataKey):
			return self.data.get(dataKey)			


test = GameConstants.instance()
print(test)
print(test.get("gridSize"))