from Avalon import Player
from Avalon import PlayerCountException, DuplicatePlayerException, NonexistentPlayerException, IncorrectStateException

import json
from random import shuffle

class AvalonGame:
    """Encapsulates game logic"""

    def __init__(self, players, config):
        """ Initializes a game with the number of players and ruleset specified

        Args:
            players (:obj:`list` of :obj:`str`): List of player names
            config (string): Path to configuration file (determines ruleset)

        """
        self._players_names = players
        self.config = json.loads(open(config,"r").read())

        self.roles = self.config['players']
        self.missions = self.config['missions']
        self.merlin_visible = self.config['merlin_visible'];
        self.evil_visible = self.config['evil_visible'];
        self.percival_visible = self.config['percival_visible'];

        self._players = dict()
        self.reset()

    def reset(self):
        """ Resets game state to starting state """
        self._state = 0
        self._game_board = [0,0,0,0,0]
        self._hammer = 0
        self._day = 0
        self._turn = 0
        self._votes = list()
        self.assign_roles()

    def assign_roles(self):
        """ Assigns roles to players """
        roles = list(self.roles[len(self._players_names)])
        shuffle(roles)
        self._players = {player_name : Player(player_name,roles.pop()) for player_name in self._players_names}

    def get_merlin_visible(self):
        """ Gets players visible by Merlin
        
        Returns:
            :obj:`list` of :obj:`str`: List of player_names of the players Merlin can see
        """

        return [player for player in self._players if (self._players[player].role in self.merlin_visible)]

    def get_evil_visible(self):
        """ Gets players visible by Evils
        
        Returns:
            :obj:`list` of :obj:`str`: List of player_names of the players Evils can see
        """

        return [player for player in self._players if (self._players[player].role in self.evil_visible)]

    def get_percival_visible(self):
        """ Gets players visible by Percival
        
        Returns:
            :obj:`list` of :obj:`str`: List of player_names of the players Percival can see
        """

        return [player for player in self._players if (self._players[player].role in self.percival_visible)]

    def check_win(self):
        """ Checks if either good or evil have won
        
        Returns:
            int: Returns -1, 0, or 1 depending on which side won
                -1: Evil win
                 0: No win (incomplete game)
                 1: Good win
        """
        if (self.game_board.count(-1) >= 3):
            return -1
        elif (self.game_board.count(1) >= 3):
            return 1
        return 0

    def get_turn_player_name(self):
        """ Gets the name of the player whose turn it is

        Returns:
            str: name of the player whose turn it is
        """
        return self.player_names[self._turn]

    def get_player_count_for_team(self):
        """ Gets the number of players for the team on the day 

        Returns:
            int: number of players for the team on the day
        """
        return self.missions[len(self._players)][self._day][0]

    def check_if_team_valid(self, players):
        """ Checks if the provided team is valid given the day and number of players and sets self._current_team equal to it if so
        
        Args:
            players (:obj:`list` of :obj:`string`): List of player names

        Returns:
            bool: whether the team is valid or not (will always be True, as failure raises a descriptive exception)

        Raises:
            PlayerCountException: if the number of players is incorrect
            DuplicatePlayersException: if there are multiple instances of a player on the team
            NonexistentPlayerException: if there is a name on the team that does not correspond to a player on the team
            IncorrectStateException: if self._state != 0
        """
        if self._state != 0:
            raise IncorrectStateException(self._state, 0)
        if (len(players) != self.missions[len(self._players)][self._day][0]):
            raise PlayerCountException(len(players), self.missions[len(self._players)][self._day][0])
        
        for player in players:
            if player not in self._players_names:
                raise NonexistentPlayerException(player)
            if players.count(player) > 1:
                raise DuplicatePlayersException(player)

        self._current_team = players
        self.increment_state()

        # if hammer has been hit (that is, hammer = 4), we can skip approval state (state 2)
        if self._hammer >= 4:
            self.increment_state()

        return True

    def check_if_approved(self, votes):
        """ Checks if the team has been approved
        
        Args:
            votes (:obj:`list` of :obj:`bool`): List of booleans describing votes (order should correspond to the order of the players in self._player_names)

        Returns: 
            bool: True if the team was approved, False otherwise

        Raises:
            PlayerCountException: if the number of votes is not equal to the number of players
            IncorrectStateException: if self._state != 1

        """
        if self._state != 1:
            raise IncorrectStateException(self._state, 1)
        if len(votes) != len(self._players):
            raise PlayerCountException(len(votes), len(self._players))

        self._votes.append(votes)

        if votes.count(False) >= len(votes)/2:
            self.increment_hammer()
            self.increment_turn()
            return False
        self.increment_state()
        return True

    def check_if_success(self, success):
        """ Checks if the mission has succeeded
        
        Args:
            votes (:obj:`list` of :obj:`bool`): List of booleans describing success/fail

        Returns: 
            bool: True if the mission succeeded, False otherwise

        Raises:
            PlayerCountException: if the number of success/fails was not equal to the number of players on the current team
            IncorrectStateException: if self._state != 2

        """
        if self._state != 2:
            raise IncorrectStateException(self._state, 2)

        if len(success) != len(self._current_team):
            raise PlayerCountException(len(success), len(self._current_team))

        self.increment_turn()
        self.increment_day()
        self.reset_hammer()
        self.increment_state()

        if success.count(False) >= self.missions[len(self._players)][self._day][1]:
            return False

        return True

    def increment_state(self):
        """ Increments _state """
        self._state = self._state + 1 % 3

    def increment_day(self):
        """ Increments _day """
        self._day += 1

    def reset_hammer(self):
        self._hammer = 0

    def increment_hammer(self):
        """ Increments _hammer """
        self._hammer += 1

    def increment_turn(self):
        """ Incrments _turn """
        self._turn = self._turn + 1 % len(_players)

    @property
    def current_team(self):
        """:obj:`list` of :obj:`str`: list of players on the current team"""
        return self._current_team
    
    @property
    def approved(self):
        """bool: flag for if self._current_team has been approved"""
        return self._approved
    

    @property
    def votes(self):
        """ :obj:`list` of :obj:`list` of :obj:`bool`: Vote history for the current game """
        return self._votes
    
    @property
    def players_names(self):
        """:obj:`list` of :obj:`str`: list of player names

        Order in list corresponds to turn order
        """
        return self._players_names
    

    @property
    def players(self):
        """ :obj:`dict` of keys :obj:`string` and values :obj:`Player`: dictionary with player names keyed to their Player objects """
        return self._players

    @property
    def state(self):
        """int: Internal state tracking variable 
        
        Should never be called externally, but Python does not have a way to make class methods or properties private.
        """
        return self._state

    @property
    def game_board(self):
        """ :obj:`list` of :obj:`str`: Game board tracker


        List of length 5, where each element can be either -1, 0, or 1.
        -1 : Failed
         0 : Not finished
         1 : Succeeded
        """
        return self._game_board
    
    @property
    def hammer(self):
        """ int: Hammer position tracker

        Ranges from 0 to 4. When hammer hits 4 the person deciding on a team chooses a team without putting it up to a vote

        """
        return self._hammer

    @property
    def day(self):
        """ int: Day tracker

        Ranges from 1 to 5.
        """
        return self._day

    @property
    def turn(self):
        """ int: Turn tracker.
        
        Ranges from 0 to self.players-1. Tracks which player's turn it is.
        """
        return self._turn
    
    