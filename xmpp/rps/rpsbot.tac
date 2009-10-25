# -*- mode: python -*-
# rpsbot.tac
from twisted.application import service
from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient

from rpsbot import RPSProtocol

application = service.Application("rpsbot")

xmppclient = XMPPClient(jid.internJID("test@thetofu.com/echobot"), "test")
#xmppclient = XMPPClient(jid.internJID("test@localhost/echobot"), "test")
xmppclient.logTraffic = True
echobot = RPSProtocol()
echobot.setHandlerParent(xmppclient)
xmppclient.setServiceParent(application)
