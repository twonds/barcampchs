# basic rock, papers, scissors logic
#

class RPS(object):
    """A simple rock, paper scissors game class.
    """

    def __init__(self):
        self.players = {}
        self.moves   = {}

        self.gameid  = 1

    def move(self, player, move):
        """ move - Send either rock, paper, or scissors to make your move.
        """
        self.moves[player] = move
        

    def join(self, player):
        """ join - Join a game of rock, paper, scissors.
        """
        if len(self.players.keys()) > 3:
            self.gameid += 1

        self.players[player] = self.gameid
        

    def help(self):
        """ help - Get help on commands.
        """
    
        commands = str(self.__doc__)"\nCommands : "
        for command in dir(self):
            if  str(type(getattr(command))) == "<type 'instancemethod'>":
                commands += "\n "+ str(getattr(self, command).__doc__)
                
        return commands
