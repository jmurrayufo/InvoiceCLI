
import uuid

from . import SQL
from .Helpers import prompt_text, prompt_float

class Item:


    db = SQL.SQL()


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
        # print(kwargs)
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.amount = float(kwargs.get('amount',0.0))
        self.quantity = float(kwargs.get('quantity',1.0))
        self.discount = float(kwargs.get('discount',0.0))
        self.tax = float(kwargs.get('tax',0.0))
        self.item_id = kwargs.get('item_id', uuid.uuid1())
        self.invoice_id = kwargs.get('invoice_id')


    def __str__(self):
        return f"{self.name} -- ${self.amount-self.discount:,.2f} x {self.quantity:.1f} + {self.tax:.2%}(tax) = ${self.total:,.2f}"


    def card(self):
        return ""


    @property
    def total(self):
        return (self.amount - self.discount) * self.quantity * (1+self.tax)


    def save_to_db(self, commit=False):
        self.db.put_item(self)
        if commit:
            self.db.commit()


    def prompt_edit_item(self):
        print("\nNew Item")
        print("Press enter to leave fields as they are, or type a value.")
        print("Press ctrl+c to go back")
        print("Press ctrl+d to go back a value")
        state = 0
        while 1:
            try:
                if state == 0:
                    print(f"Name: {self.name}")
                    data = prompt_text("> ")
                    if data is not None:
                        self.name = data
                if state == 1:        
                    print(f"Description: {self.description}")
                    data = prompt_text("> ")
                    if data is not None:
                        self.description = data
                if state == 2:        
                    print(f"Amount: {self.amount}")
                    data = prompt_float("> ")
                    if data is not None:
                        self.amount = data
                if state == 3:        
                    print(f"Quantity: {self.quantity}")
                    data = prompt_float("> ")
                    if data is not None:
                        self.quantity = data
                if state == 4:        
                    print(f"Discount: {self.discount}")
                    data = prompt_float("> ")
                    if data is not None:
                        self.discount = data
                if state == 5:        
                    print(f"Tax: {self.tax}")
                    print("Enter actual percentage, not the true floating point value")
                    data = prompt_float("> ")
                    if data is not None:
                        # Note that tax is auto converted 
                        self.tax = data/100
                if state == 6:        
                    self.item_id = uuid.uuid1()
                if state >= 7:
                    print("Final check before finishing edits.")
                    print(self)
                    print("Press enter to finish, or ctrl+d to go back")
                    input("> ")
                    return True
            except EOFError as e:
                print()
                state -= 2
            state += 1

