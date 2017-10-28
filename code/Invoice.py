
import datetime
import uuid

from . import Item
from . import SQL
from .Helpers import prompt_text, prompt_valid_index


class Invoice:


    db = SQL.SQL()


    def __init__(self,**kwargs):
        self.name = kwargs.get('name', 'NO NAME')
        self.description = kwargs.get('description', None)
        self.invoice_id = kwargs.get('invoice_id', uuid.uuid1())
        self.client_id = kwargs.get('client_id')
        self.items = kwargs.get('items', [])
        self.created = kwargs.get('created', datetime.datetime.now())
        self.due = kwargs.get('due', datetime.date.today())
        self.state = kwargs.get('state', "UNINIT")

        if type(self.due) is str:
            self.due = datetime.datetime.strptime(self.due,"%Y-%m-%d").date()

        if type(self.created) is str:
            self.created = datetime.datetime.strptime(self.created,"%Y-%m-%dT%H:%M:%S")

        if type(self.invoice_id) is str:
            self.invoice_id = uuid.UUID(self.invoice_id)


    def __str__(self):
        if self.state == 'PAID':
            return f"[{self.state}] {self.name} due {self.due} ({(self.due-datetime.date.today()).total_seconds()/(24*60*60):.0f} days)"
        else:
            return f"[{self.state}] {self.name} ${self.total:,.2f} due {self.due} ({(self.due-datetime.date.today()).total_seconds()/(24*60*60):.0f} days)"


    def card(self):
        ret_val = ""
        ret_val += f"Name: {self.name}"
        ret_val += f"\n  Description: {self.description}"
        client_dict = self.db.get_client(client_id=self.client_id)
        ret_val += f"\n  Client: {client_dict['first_name']} {client_dict['last_name']}"
        ret_val += f"\n  Created: {self.created}"
        ret_val += f"\n  Due: {self.due}"
        ret_val += f"\n  State: {self.state}"
        ret_val += f"\n  Items"
        ret_val += f"\n  -----"
        for item in self.items:
            ret_val += f"\n  {item}"
        return ret_val


    @property
    def total(self):
        ret_val = 0.0
        for item in self.items:
            ret_val += item.total
        return ret_val


    def save_to_db(self):
        self.db.put_invoice(self)
        for item in self.items:
            item.save_to_db()
        self.db.commit()


    def prompt_new_invoice(self, client=None):
        if client is not None:
            self.client_id = client.client_id
        print("\nInvoice Editor")
        self.state = "NEW"
        while 1:
            print(self.card())
            print()
            print("[1] New Item")
            print("[2] Edit Item")
            print("[3] Delete Item")
            print("[4] Edit Detail")
            print("[s] Save and Exit")
            print("[q] Exit w/o Saving")
            selection = prompt_text("> ")

            if selection == '1':
                try:
                    item = Item.Item()
                    item.prompt_edit_item()
                except KeyboardInterrupt:
                    print("Caught keyboard interrupt, no item added.")
                    continue
                item.invoice_id = self.invoice_id
                self.items.append(item)
                pass

            elif selection == '2':
                if len(self.items) == 0:
                    print("No items to edit")
                    continue
                print("Items to edit:")
                for idx,item in enumerate(self.items):
                    print(f"[{idx}] {item}")
                print("Which item?")
                print("Press enter to skip.")
                try:
                    selection = prompt_valid_index("> ",range(len(self.items)))
                except KeyboardInterrupt:
                    continue
                except ValueError:
                    print("Invalid input, returning to menu.")
                    continue
                self.items[selection].prompt_edit_item()
                self.items[selection]

            elif selection == '3':
                if len(self.items) == 0:
                    print("No items to delete")
                    continue

            elif selection == '4':
                self._edit_details()

            elif selection == 's':
                self.save_to_db()
                print("Saved.")
                return

            elif selection == 'q':
                return


    def _edit_details(self):
        print("\nInvoice Details")
        print("Press enter to leave fields as they are, or type a value.")
        print("Press ctrl+c to quit")
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
                    print(f"Due: {self.due}")
                    print("Format string is YYYY-MM-DD")
                    data = prompt_text("> ")
                    if data is not None:
                        try:
                            self.due = datetime.datetime.strptime(data,"%Y-%m-%d").date()
                        except:
                            raise
                if state >= 3:
                    return

            except KeyboardInterrupt as e:
                return
            except EOFError as e:
                print()
                state -= 2

            state += 1


    def load_items(self, items_list=None):
        """Load items. If given a list of valid item dicts,
        attempt to cache from them. Otherwise, use the db.
        """

        if items_list is None:
            
            for item in items_list:


