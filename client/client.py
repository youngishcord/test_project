from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as CF
from twisted.internet.endpoints import TCP4ClientEndpoint
from config.config import HOST, PORT
import json

class Client(Protocol):
    def __init__(self):
        reactor.callInThread(self.send_data)

    def dataReceived(self, data):
        data = data.decode()
        print(data)

    def connectionMade(self):
        print('Hello client')

    def send_data(self):
        while True:
            mess = input()
            if mess[0] == "!":
                if mess == "!help":
                    print("message for help")
                elif mess == "!sum":
                    try:
                        a = int(input("input arg1 "))
                        b = int(input("input arg2 "))
                        c = {"func":f"{mess[1:]}", 
                            "arg1":a, 
                            "arg2":b}
                        print(c)
                        d = json.dumps(c)
                        print(type(d))
                        self.transport.write(d.encode())
                    except ValueError:
                        print("type except")
                    except:
                        print('error')
            else:
                print("commands start at !\ninput !help for more info")
                self.transport.write(mess.encode())



class ClientFactory(CF):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        CF.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print(reason)
        CF.clientConnectionLost(self, connector, reason)


if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, HOST, PORT)
    endpoint.connect(ClientFactory())
    reactor.run()