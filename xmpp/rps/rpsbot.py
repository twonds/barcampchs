## rock, paper, scissors xmpp chat protocol
from twisted.python import log # use this for logging
from twisted.words.xish import domish # used for manipulating xml
from wokkel.xmppim import MessageProtocol, AvailablePresence # protocol helpers

import exceptions

import rps

class RPSProtocol(MessageProtocol):
    """Handle XMPP Protocol for Rock, Paper, Scissors.
    """


    def connectionMade(self):
        """This method is trigged by wokkel when 
           a connection has been established and authorized.
 
        We have authenticated and have a Jabber ID. 

        Once this is done we send presence to the server. 
        This allows others and the server to know where are available.
        """
        self.rps = rps.RPS() # game logic class

        log.msg("\n RPS has connected! \n")
        # send initial presence
        self.send(AvailablePresence())
        log.msg("\n RPS has sent presence! \n")


    def connectionLost(self, reason):
        """This method is triggered when the TCP connection is lost. 
        The parameter reason is the reason for the disconnect.
        
        We are just gonna log that it happened and ignore the reason.
        """
        log.msg("RPS has disconnected!")

    def onMessage(self, msg):
        """Handle all message types. 
        Normally, we would use xpath for different message types.
        """
        log.msg("======================== onMessage =========================")
        outcome_message = None

        if msg.hasAttribute('type') \
                and msg["type"] == 'chat' \
                and hasattr(msg, "body"):
            
            cmd = str(msg.body).lower() # clean up body for handling
            log.msg("========= trying to execute %s =============\n" % (cmd,))
            
            player = msg['from'].lower() # get our player
            log.msg("========= player %s =============\n" % (player,))
            
            if cmd == 'join':
                self._doJoin(player)
            elif cmd in self.rps.VALID_MOVES:
                self._doGameMove(player, cmd)                
            else:
                self._doHelp(player)

    def _doHelp(self, player):
        """Send help message.
        """ 
        outcome_message = self.rps.help()

        self.sendMessage(player, outcome_message)


    def _doJoin(self, player):
        """Join a game to play.
        """
        if self.rps.join(player):
            outcome_message = "You have joined the game!"
        else:
            outcome_message = "We are full."

        self.sendMessage(player, outcome_message)


    def _doGameMove(self, player, move):
        """ Make a move.
        """
        game_move = self.rps.move(player, move)
        log.msg(game_move)

        outcome_message = 'Invalid move?'

        if game_move is None:
            outcome_message = 'Game has not started.'
            if player in self.rps.players:
                outcome_message += " Please wait."
            else:
                outcome_message += " Please join."

        elif game_move == rps.WAIT_PLAYER:
            outcome_message = 'Thanks, waiting for the other player.'
        
        elif game_move == rps.DRAW:
            outcome_message = "You both played %s !" % (move,)
            for p in self.rps.players:
                if p != player:
                    self.sendMessage(p, outcome_message)
            self.rps.restart()
        
        elif game_move == rps.PLAYER1:
            outcome_message = self._wins(player, rps.PLAYER1)
        elif game_move == rps.PLAYER2:
            outcome_message = self._wins(player, rps.PLAYER2)

        self.sendMessage(player, outcome_message)


    def _wins(self, player, play):
        winner = self.rps.getPlayer(play)

        outcome_message = "Player %s wins with %s!" % (winner[0], winner[1],)

        for p in self.rps.players:
            if p != player and p != winner[0]:
                self.sendMessage(p, outcome_message)
            if p != player and p == winner[0]:
                self.sendMessage(p, "You are the winner!")

        self.rps.restart()

        if winner[0] == player:
            outcome_message = " You are the winner! "

        return outcome_message

    def sendMessage(self, to, body):
        """ Send an XMPP message stanza of type chat with a body.
        """
        reply = domish.Element(('xmpp:client', "message"))
        reply["to"] = to
        reply["type"] = 'chat'
        reply.addElement("body", content=body)

        self.send(reply)


