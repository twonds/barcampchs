# basic rock, papers, scissors logic
#

INVALID_MOVE = -2
WAIT_PLAYER = -1

DRAW = 0
PLAYER1 = 1
PLAYER2 = 2

PLAYER_COUNT = 2

class RPS(object):
    """A simple rock, paper scissors game class.
    """

    def __init__(self):
        self.start()
        self.VALID_MOVES = ['rock', 'paper', 'scissors']

    def start(self):
        self.moves = []
        self.players = []

    restart = start # magic rename

    def move(self, player, move):
        """ move - Send either rock, paper, or scissors to make your move.
        """
        cmp = WAIT_PLAYER # means game is not over.
        if len(self.players) == PLAYER_COUNT:
            if move in self.VALID_MOVES:
                self.moves.append((player, move.lower()))
                
                if len(self.moves) == PLAYER_COUNT:
                    cmp = self._cmp(self.moves[0], 
                                    self.moves[1])
                    
            else:
                cmp = INVALID_MOVE
        else:
            cmp = None # game hasnt started 
        return cmp

    def getPlayer(self, num):
        return self.moves[num-1]


    def _cmp(self, mv1, mv2):
        ret_val = DRAW

        if mv1[1] == 'rock':
            if mv2[1] == 'paper':
                ret_val = PLAYER2
            elif mv2[1] == 'scissors':
                ret_val = PLAYER1
        elif mv1[1] == 'paper':
            if mv2[1] == 'rock':
                ret_val = PLAYER1
            elif mv2[1] == 'scissors':
                ret_val = PLAYER2
        elif mv1[1] == 'scissors':
            if mv2[1] == 'paper':
                ret_val = PLAYER1
            elif mv2[1] == 'rock':
                ret_val = PLAYER2

        return ret_val
        


    def join(self, player):
        """ join - Join a game of rock, paper, scissors.
        """
        if len(self.players) > PLAYER_COUNT:
            return False
        
        self.players.append(player)
        return True

    def help(self):
        """ help - Get help on commands.
        """
        commands = str(self.__doc__)+"\nCommands : "
        for command in dir(self):
            if command[0] == '_':
                continue
            if  str(type(getattr(self, command))) == "<type 'instancemethod'>":
                doc = getattr(self, command).__doc__
                if doc is not None:
                    commands += "\n "+ str(doc)
                                 
        return commands
