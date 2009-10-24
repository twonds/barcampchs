## rock, paper, scissors xmpp chat protocol
from twisted.python import log # use this for logging
from twisted.words.xish import domish # used for manipulating xml
from wokkel.xmppim import MessageProtocol, AvailablePresence # protocol helpers



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
        log.msg("======================== onMessage =========================")
        
        if msg.hasAttribute('type') and msg["type"] == 'chat' and hasattr(msg, "body"):
            reply = domish.Element((None, "message"))
            reply["to"] = msg["from"]
            reply["from"] = msg["to"]
            reply["type"] = 'chat'
            reply.addElement("body", content="echo: " + str(msg.body))

            self.send(reply)


