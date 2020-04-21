from event import Event, Response, INVALID
import socket
import pickle

def handle():
    # receive transaction command
    # determine if valid + able to perform
    # give feedback
    #......
    # recieve do-commit message
    # perform the action
    # give feedback
    # - if not: disassemble transaction setup.
    pass

class MicroService():

    def listen(self, address):
        with socket.create_server(address) as server:
            server.listen(1)
            while True:
                conn, _ = server.accept()
                with conn:
                    message = pickle.loads(conn.recv(4096))
                    if isinstance(message, Event):
                        response = self.handle(message)
                        conn.sendall(pickle.dumps(response))
                    else:
                        conn.sendall(pickle.dumps(Response(INVALID, 'not an event...')))

    def handle(self, event: Event):
        raise NotImplementedError()

if __name__ == "__main__":
    MicroService().handle(None)
