
class Player:
	"""Storage for any relevant player data"""
	
	def __init__(self, name, role):
		"""
		Args:
			name (str): name of the player
			role (str): role of the player
		"""
		self._name = name
		self._role = role
	
	@property
	def name(self):
		""" str: Name of the player """
		return self._name
	
	@property
	def role(self):
		""" str: Role of the player """
		return self._role
	

