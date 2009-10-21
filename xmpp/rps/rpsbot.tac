# -*- mode: python -*-
# rpsbot.tac
from twisted.application import service
from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient

from rpsbot import RPSProtocol

application = service.Application("rpsbot")

xmppclient = XMPPClient(jid.internJID("someuser@example.com/echobot"), "pass")
xmppclient.logTraffic = False
echobot = RPSProtocol()
echobot.setHandlerParent(xmppclient)
xmppclient.setServiceParent(application)
