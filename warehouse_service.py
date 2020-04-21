import sys
import logging
from event import *
from model.warehouse import Warehouse, Item
from microservice import MicroService

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

ADDRESS = ('', int(sys.argv[2]))
transactions = {}
warehouse = Warehouse(sys.argv[1])
warehouse.add_item(Item('stonk', 9000, 255))

def prepare(event: Event) -> Response:
    if isinstance(event, TransferEvent):
        item: Item = event.item
        if event.source == warehouse.name:
            our_item = warehouse.get_item(item.name)
            if our_item:
                if our_item.amount >= item.amount:
                    logging.debug(f'We have {our_item} and shall subtract {item}')
                    return Response(OK, 'ok we can give dis')
                else:
                    return Response(ERROR, 'not enough left')
            else:
                return Response(ERROR, 'not in stock')
        elif event.destination == warehouse.name:
            logging.debug(f'yeah ok sure, we have {warehouse.get_item(item.name)}')
            return Response(OK, 'ok we\'ll see')
        else:
            return Response(INVALID, 'I am not involved')
    elif isinstance(event, LossEvent):
        item: Item = event.item
        our_item = warehouse.get_item(item.name)
        if our_item:
            if our_item.amount >= item.amount:
                logging.debug(f'We have {our_item} and shall subtract {item}')
                return Response(OK, 'ok we may have lost dis')
            else:
                return Response(ERROR, 'not enough left to loose')
        else:
                return Response(INVALID, 'not in stock')
    elif isinstance(event, GainEvent):
        return Response(OK, 'welll sure we can do that')
    else:
        return Response(INVALID, 'not a known event')

def commit(event: Event) -> Response:
    if isinstance(event, TransferEvent):
        item = event.item
        if event.source == warehouse.name:
            our_item = warehouse.get_item(item.name)
            if our_item:
                if our_item.amount >= item.amount:
                    our_item.amount -= item.amount
                    logging.debug(f'there is now {our_item}')
                    return Response(OK, 'ok it is given')
                else:
                    return Response(ERROR, 'not enough left')
            else:
                return Response(ERROR, 'not in stock')
        elif event.destination == warehouse.name:
            warehouse.add_item(item)
            logging.debug(f'there is now {warehouse.get_item(item.name)}')
            return Response(OK, 'i got it!')
        else:
            return Response(INVALID, 'I am not involved')
    elif isinstance(event, LossEvent):
        item: Item = event.item
        our_item = warehouse.get_item(item.name)
        if not our_item:
            return Response(ERROR, 'not in stock')
        
        if warehouse.subtract_item(item):
            logging.debug(f'there is now {our_item}')
            return Response(OK, 'loss enacted')
        else:
            return Response(ERROR, 'cannot have lost that much')
    elif isinstance(event, GainEvent):
        item: Item = event.item
        warehouse.add_item(item)
        logging.debug(f'there is now {warehouse.get_item(item.name)}')
        return Response(OK, 'gain enacted')
    else:
        return Response(INVALID, 'not a known event')

def rollback(event: Event) -> Response:
    if isinstance(event,TransferEvent):
        item = event.item
        our_item = warehouse.get_item(item.name)
        if not our_item:
            return Response(ERROR, 'not in stock')
        
        if event.source == warehouse.name:
            warehouse.add_item(item)
            logging.debug(f'rollback: there is now {our_item}')
            return Response(OK, 'got it back')
        elif event.destination == warehouse.name:
            if warehouse.subtract_item(item):
                logging.debug(f'rollback: there is now {our_item}')
                return Response(OK, 'removed it')
            else:
                return Response(ERROR, 'cannot subtract that')
        else:
            return Response(INVALID, 'I am not involved')
    elif isinstance(event, LossEvent):
        item: Item = event.item
        warehouse.add_item(item)
        logging.debug(f'there is now {warehouse.get_item(item.name)}')
        return Response(OK, 'rollback: added back the lost stuff')
    elif isinstance(event, GainEvent):
        item: Item = event.item
        our_item = warehouse.get_item(item.name)
        if not our_item:
            return Response(ERROR, 'not in stock')
        
        if warehouse.subtract_item(item):
            logging.debug(f'there is now {our_item}')
            return Response(OK, 'rollback: removed added items')
        else:
            return Response(ERROR, 'cannot have gained any?')
    else:
        return Response(INVALID, 'not a known event')

def abort(event: Event) -> Response:
    # only relevant once there's some action log...
    return Response(OK, 'i guess it won\'t happen then')

action_map = {
    PREPARE: prepare,
    COMMIT: commit,
    ROLLBACK: rollback,
    ABORT: abort
}

class WarehouseService(MicroService):
    def handle(self, message: Event):
        try:
            return action_map[message.state](message)
        except KeyError as e:
            logging.error(f'stuff {message.id} and {e}')
            return Response(FAILURE, 'Invalid message')
        return Response(FAILURE, 'idk')

service = WarehouseService()
service.listen(ADDRESS)
