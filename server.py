from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import  ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
import ctypes, sys

class Server(Protocol):
    def connectionMade(self):
        print("[!] New connection detected from" + "X.X.X.X")
        self.transport.write("".encode("utf-8"))
        self.transport.loseConnection()


class ServerFactory(ServFactory):
    def buildProtocol(self, addr):
        return Server()

if __name__ == "__main__":
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        endpoint = TCP4ServerEndpoint(reactor, 6667)
        endpoint.listen(ServerFactory())
        reactor.run()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
