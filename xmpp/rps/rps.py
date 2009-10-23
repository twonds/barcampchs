# basic rock, papers, scissors logic
#

class RPS(object):
    """A simple rock, paper scissors game class.
    """

    def __init__(self):
        self.players = []
        self.moves   = []
        self.VALID_MOVES = ['rock', 'paper', 'scissors']

    def move(self, player, move):
        """ move - Send either rock, paper, or scissors to make your move.
        """
        cmp = -1 # -1 means game is not over.
        if len(self.players) == 2:
            if move in self.VALID_MOVES:
                self.moves.append((player, move.lower()))
                
                if len(self.moves) == 2:
                    cmp = self._cmp(self.moves[0][1], 
                                    self.moves[1][1])
            else:
                cmp = -2 
        else:
            cmp = None # game hasnt started 
        return cmp


    def _cmp(self, mv1, mv2):
        ret_val = 0
        if mv1[1] == 'rock':
            if mv2[1] == 'paper':
                ret_val = 2
            elif mv2[1] == 'scissors':
                ret_val = 1
        elif mv1[1] == 'paper':
            if mv2[1] == 'rock':
                ret_val = 1
            elif mv2[1] == 'scissors':
                ret_val = 2
        elif mv1[1] == 'scissors':
            if mv2[1] == 'paper':
                ret_val = 1
            elif mv2[1] == 'rock':
                ret_val = 2

        return ret_val
        
    def _tcmp(self, mv1, mv2):
        ret_val = 0 # zero is a tie
        if mv1 == 'rock' and mv2 == 'paper':
            ret_val = 2
        elif mv1 == 'scissors' and mv2 == 'rock':
            ret_val = 2
        elif mv1 == 'scissors' and mv2 == 'rock':
            ret_val = 2
        elif mv2 == 'rock' and mv1 == 'paper':
            ret_val = 1
        elif mv2 == 'scissors' and mv1 == 'rock':
            ret_val = 1
            

        return ret_val

    def join(self, player):
        """ join - Join a game of rock, paper, scissors.
        """
        if len(self.players) > 2:
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
            if  str(type(getattr(command))) == "<type 'instancemethod'>":
                commands += "\n "+ str(getattr(self, command).__doc__)
                
        return commands
