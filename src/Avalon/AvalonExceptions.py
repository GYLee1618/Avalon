class PlayerCountException(Exception):
""" Exception thrown when the game is given a different number of players than expected """
    
    def __init__(self, number, expected):
    """ Constructor
	
	Args:
		number (int): the number of players on the team
		expected (int): the number of players expected
    """
        Exception.__init__(self, "Expected {} players, got {} instead.".format(number, expected))

class DuplicatePlayerException(Exception):
""" Exception thrown when the game is given duplicate players on a team """

	def __init__(self, player):
	""" Constructor

	Args:
		player (str): name of player with duplicate entry
	"""
		Exception.__init__(self, "Found multple instances of {} on team. Players cannot be on teams more than once.".format(player))

class NonexistentPlayerException(Exception):
""" Exception thrown when the game is given a name that does not correspond to a player in the game """

	def __init__(self, name):
	""" Constructor

	Args:
		name (str): name that does not correspond to player in game
	"""
		Exception.__init__(self, "Name {} does not correspond to any players in the game.".format(player))

class IncorrectStateException(Exception):
"""Exception thrown when an action is taken out of state

Args:
	current_state (int): the current state value of the Avalon object
	expected_state (int): the expected state value of the Avalon object

"""
	def __init__(self,current_state,expected_state):
	""" Constructor """
        Exception.__init__(self, "Expected to be in state {}, in state {} instead.".format(current_state, expected_state))