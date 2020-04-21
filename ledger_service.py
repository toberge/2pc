from microservice import MicroService
from event import Event, Response, OK, COMMIT
import sys

class LedgerService(MicroService):
    def handle(self, event: Event):
        if event.state == COMMIT:
            print(event) # temp cop-out
        return Response(OK, 'ok i am fine')

ADDRESS = ('', int(sys.argv[1]))
service = LedgerService()
service.listen(ADDRESS)
