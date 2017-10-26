
import datetime
from . import Item


class Invoice:

    def __init__(self,**kwargs):
        self.name = kwargs.get('name', 'NO NAME')
        self.description = kwargs.get('description', None)
        self.invoice_id = kwargs.get('invoice_id', uuid.uuid1())
        self.client_id = kwargs.get('client_id')
        self.items = kwargs.get('items', [])
        self.created = kwargs.get('created', datetime.datetime.now())
        self.due = kwargs.get('created', datetime.datetime.now())
        self.state = kwargs.get('state', "UNINIT")


    @property
    def total(self):
        ret_val = 0.0
        for item in self.items:
            ret_val += item.total

        return ret_val
