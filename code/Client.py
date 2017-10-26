
import uuid
import datetime


from . import Invoice
from . import SQL
from .Helpers import prompt_text

class Client:

    db = None
    def __init__(self,*args,**kwargs):
        if self.db == None:
            self.db = SQL.SQL()
        self.first_name = kwargs.get('first_name', None)
        self.last_name = kwargs.get('last_name', None)
        self.email = kwargs.get('email', None)
        self.address = kwargs.get('address', None)
        self.state = kwargs.get('state', None)
        self.city = kwargs.get('city', None)
        self.zip_code = kwargs.get('zip_code', None)
        self.client_id = kwargs.get('client_id', None)
        self.invoices = kwargs.get('invoices', None)
        self.created = kwargs.get('created',None)

        if self.client_id is None:
            try:
                db_dict = self.db.get_client(first_name=self.first_name, last_name=self.last_name)
                self.first_name = db_dict.get('first_name', None)
                self.last_name = db_dict.get('last_name', None)
                self.email = db_dict.get('email', None)
                self.address = db_dict.get('address', None)
                self.state = db_dict.get('state', None)
                self.city = db_dict.get('city', None)
                self.zip_code = db_dict.get('zip_code', None)
                self.client_id = db_dict.get('client_id', None)
                self.invoices = db_dict.get('invoices', None)
                self.created = db_dict.get('created',None)
            except ValueError:
                self.client_id = uuid.uuid1()
                self.created = datetime.datetime.now()


    def __repr__(self):
        return f"Client(name='{self.first_name} {self.last_name}', id={self.client_id})"


    def __str__(self):
        return f"{self.first_name} {self.last_name}"\
        +f"\n  {self.email}"\
        +f"\n  {self.address}"\
        +f"\n  {self.city}, {self.state} {self.zip_code}"


    @property
    def balance(self):
        # TODO: Query DB for all our invoices, and print the current balance
        return 0


    def save_to_db(self):
        self.db.put_client(self)


    # GUI Link Functions
    def prompt_edit_user(self):
        print("\nUser Editor")
        print("Press enter to leave fields as they are, or type a value.")
        print("Press ctrl+c to quit")
        print("Press ctrl+d to go back a value")
        state = 0
        while state < 7:
            try:
                if state == 0:
                    print(f"First Name: {self.first_name}")
                    data = prompt_text("> ")
                    if data != '':
                        self.first_name = data
                if state == 1:        
                    print(f"Last Name: {self.last_name}")
                    data = prompt_text("> ")
                    if data != '':
                        self.last_name = data
                if state == 2:        
                    print(f"E-Mail: {self.email}")
                    data = prompt_text("> ")
                    if data != '':
                        self.email = data
                if state == 3:        
                    print(f"Address: {self.address}")
                    data = prompt_text("> ")
                    if data != '':
                        self.address = data
                if state == 4:        
                    print(f"State: {self.state}")
                    data = prompt_text("> ")
                    if data != '':
                        self.state = data
                if state == 5:        
                    print(f"City: {self.city}")
                    data = prompt_text("> ")
                    if data != '':
                        self.city = data
                if state == 6:        
                    print(f"Zip: {self.zip_code}")
                    data = prompt_text("> ")
                    if data != '':
                        self.zip_code = data

            except KeyboardInterrupt as e:
                return
            except EOFError as e:
                print()
                state -= 2

            state += 1

        print("Final check before saving edits.")
        print(self)
        print("Is the above correct?")
        if input("(yes/no)> ").startswith(('y','Y')):
            self.save_to_db()

        
