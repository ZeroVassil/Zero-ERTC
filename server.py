from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import  ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

class Server(Protocol):
    def __init__(self, users):
        self.users = users
        self.name = ""

    def connectionMade(self):
        print("[!] New connection detected from " + str(self))
        self.transport.write("Welcome to X.X.X.X aes-256 encrypted communication channel".encode("utf-8"))

    def addUser(self, name):
        if name not in self.users:
            self.users[self] = name
            self.name = name
        else:
            self.transport.write("Invalid username (most commonly caused by using a username already registered by another user)".encode("utf-8"))

    def connectionLost(self, reason=connectionDone):
        del self.users[self]

    def dataReceived(self, data):
        data = data.decode("utf-8")

        if not self.name:
            self.addUser(data)
            return
        for protocol in self.users.keys():
            if protocol != self:
                protocol.transport.write(f"{self.name}: {data}".encode("utf-8"))


class ServerFactory(ServFactory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Server(self.users)

if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 6667)
    endpoint.listen(ServerFactory())
    reactor.run()
