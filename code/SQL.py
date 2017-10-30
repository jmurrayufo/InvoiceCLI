from pathlib import Path
import json
import logging
import os
import shutil
import sqlite3
import time


class SQL:
    c = None
    conn = None
    log = logging.getLogger('ICLI').getChild(__name__)


    def __init__(self):

        db_file = Path('local_cache.db')
        if not db_file.is_file():
            self.initalize()
        if SQL.conn is None:
            print("CONNECTION")
            self.log.info("Attempt to connect to SQL local db")
            SQL.conn = sqlite3.connect(str(db_file))
            SQL.conn.row_factory = self.dict_factory
            SQL.c = SQL.conn.cursor()
            # SQL.c.arraysize = 300
            self.log.info("Connected")


    def commit(self):
        SQL.conn.commit()


    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def initalize(self):
        # Init the connection

        SQL.conn = sqlite3.connect('local_cache.db')
        SQL.conn.row_factory = self.dict_factory
        SQL.c = SQL.conn.cursor()

        # Add tables as needed
        self.log.info("Create config table")
        SQL.c.execute("""
            CREATE TABLE IF NOT EXISTS config
            (
                key text UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
            """)

        self.log.info("Create clients table")
        SQL.c.execute("""
            CREATE TABLE IF NOT EXISTS clients
            (
                client_id TEXT UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                address TEXT,
                state TEXT,
                city TEXT,
                zip_code TEXT,
                created TEXT
            )
            """)

        self.log.info("Create invoices table")
        SQL.c.execute("""
            CREATE TABLE IF NOT EXISTS invoices
            (
                invoice_id TEXT UNIQUE NOT NULL ON CONFLICT FAIL,
                name TEXT,
                description TEXT,
                client_id TEXT NOT NULL,
                created TEXT,
                due TEXT,
                state TEXT
            )
            """)

        self.log.info("Create items table")
        SQL.c.execute("""
            CREATE TABLE IF NOT EXISTS items
            (
                item_id TEXT UNIQUE NOT NULL,
                name TEXT,
                description TEXT,
                amount REAL,
                quantity REAL,
                discount REAL,
                tax REAL,
                invoice_id TEXT NOT NULL
            )
            """)

        # self.log.info("Create orders table")
        # SQL.c.execute("""
        #     CREATE TABLE IF NOT EXISTS  orders
        #     (
        #         order_id INTEGER UNIQUE NOT NULL,
        #         duration INTEGER,
        #         is_buy_order BOOLEAN,
        #         issued REAL,
        #         location_id INTEGER,
        #         min_volume INTEGER,
        #         price REAL,
        #         range TEXT,
        #         recorded REAL,
        #         region_id INTEGER NOT NULL,
        #         type_id INTEGER,
        #         volume_remain INTEGER,
        #         volume_total INTEGER
        #     )
        #     """)
        # SQL.c.execute("""
        #     CREATE INDEX IF NOT EXISTS ordersItypeid
        #     ON orders(type_id)
        #     """)
        # SQL.c.execute("""
        #     CREATE INDEX IF NOT EXISTS ordersIregionid
        #     ON orders(region_id)
        #     """)
        # SQL.c.execute("""
        #     CREATE INDEX IF NOT EXISTS ordersIcombo
        #     ON orders(type_id,region_id)
        #     """)

        # self.log.info("Create histories table")
        # SQL.c.execute("""
        #     CREATE TABLE IF NOT EXISTS  histories
        #     (
        #         type_id INTEGER NOT NULL,
        #         date TEXT NOT NULL,
        #         highest REAL,
        #         lowest REAL,
        #         order_count INTEGER,
        #         volume INTEGER
        #     )
        #     """)
        SQL.conn.commit()


    ####################
    ## Client Methods ##
    ####################

    def get_client(self, client_id=None, first_name=None, last_name=None):
        """
        Raises
            ValueError -- Didn't find one, and only one, client.
        """
        if first_name is not None and last_name is not None:
            SQL.c.execute(
                "SELECT * FROM clients WHERE (first_name=? AND last_name=? )",
                (first_name,last_name))
        elif first_name is not None:
            SQL.c.execute(
                "SELECT * FROM clients WHERE (first_name=?)",
                (first_name,))
        elif last_name is not None:
            SQL.c.execute(
                "SELECT * FROM clients WHERE (last_name=?)",
                (last_name,))
        elif client_id is not None:
            SQL.c.execute(
                "SELECT * FROM clients WHERE (client_id=?)",
                (str(client_id),))
        else:
            raise ValueError("Must be given either a first or last name!")

        data = SQL.c.fetchall()
        if not len(data) == 1:
            raise ValueError(f"Didn't find one, and only one, entry with given input of first_name: {first_name} and last_name: {last_name}")
        return data[0]


    def get_clients(self):
        SQL.c.execute("SELECT * FROM clients")
        return SQL.c.fetchall()


    def put_client(self,client):
        SQL.c.execute("""
            INSERT OR REPLACE INTO clients 
            (
             client_id,
             first_name,
             last_name,
             email,
             address,
             state,
             city,
             zip_code,
             created
             )
            VALUES
            (?,?,?,?,?,?,?,?,?)""",
            (str(client.client_id),
             client.first_name,
             client.last_name,
             client.email,
             client.address,
             client.state,
             client.city,
             client.zip_code,
             client.created.isoformat(timespec='seconds')
             )
            )
        # SQL.conn.commit()



    #####################
    ## Invoice Methods ##
    #####################

    def get_invoice(self,**kwargs):
        pass

    def get_invoices(self):
        SQL.c.execute("SELECT * FROM invoices")
        return SQL.c.fetchall()

    def get_invoices_ex(self):
        pass

    def put_invoice(self,invoice,new=False):
        SQL.c.execute("""
            INSERT OR REPLACE INTO invoices 
            (
             client_id,
             invoice_id,
             name,
             description,
             created,
             due,
             state
             )
            VALUES
            (?,?,?,?,?,?,?)""",
            (str(invoice.client_id),
             str(invoice.invoice_id),
             invoice.name,
             invoice.description,
             invoice.created.isoformat(timespec='seconds'),
             invoice.due.isoformat(),
             invoice.state,
             )
            )
        # SQL.conn.commit()


    #####################
    ## Item Methods ##
    #####################

    def get_item(self,**kwargs):
        pass

    def get_items(self):
        SQL.c.execute("SELECT * FROM items")
        return SQL.c.fetchall()

    def put_item(self,item,new=False):
        SQL.c.execute("""
            INSERT OR REPLACE INTO items 
            (
             item_id,
             invoice_id,
             name,
             description,
             amount,
             quantity,
             discount,
             tax
             )
            VALUES
            (?,?,?,?,?,?,?,?)""",
            (str(item.item_id),
             str(item.invoice_id),
             item.name,
             item.description,
             item.amount,
             item.quantity,
             item.discount,
             item.tax
             )
            )
        # SQL.conn.commit()
