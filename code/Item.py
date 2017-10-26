
import uuid

class Item:


    def __init__(self,**kwargs):
        """
            Keyword Arguments:
            name -- Simple name of item
            description -- Long description, and more details, of item
            amount -- Cost (or credit if negative) per unit
            quantity -- Total units, partial allowed'
            discount -- Cost reduction per unit
            tax -- % tax applied to total after discount
            id -- Unique id applied to Item (Items may share the same name/description, but id should always be unique)
        """
        self.name = kwargs.get('name', 'NO NAME')
        self.description = kwargs.get('description', None)
        self.amount = float(kwargs.get('amount',0.0))
        self.quantity = float(kwargs.get('quantity',1.0))
        self.discount = float(kwargs.get('discount',0.0))
        self.tax = float(kwargs.get('tax',0.0))
        self.item_id = kwargs.get('item_id', uuid.uuid1())
        self.invoice_id = kwargs.get('invoice_id')


    @property
    def total(self):
        return (self.amount - self.discount) * self.quantity * (1+self.tax)