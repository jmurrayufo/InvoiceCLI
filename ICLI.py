#!/usr/bin/env python3

import readline
import time
import argparse


from code import Client, Invoice


parser = argparse.ArgumentParser(
    description="Invoice Command Line Interface",
    )

parser.add_argument(
    "--add-client","--ac",
    action='store_true',
    help='Add a new client')
parser.add_argument(
    "--edit-client","--ec",
    action='store_true',
    help='Edit an existing client')

parser.add_argument(
    "--new-invoice","--ni",
    action='store_true',
    help='Create a new invoice')
parser.add_argument(
    "--duplicate-invoice","--di",
    action='store_true',
    help='Create a duplicate invoice')
parser.add_argument(
    "--edit-invoice","--ei",
    action='store_true',
    help='Edit an invoice')
parser.add_argument(
    "--list-invoice","--li",
    action='store_true',
    help='List invoices')
parser.add_argument(
    "--list-active-invoice","--lai",
    action='store_true',
    help='List invoices')

args = parser.parse_args()
print(args)

if args.add_client:
    client = Client.Client()
    client.prompt_edit_user()

if args.edit_client:
    client = Client.Client.prompt_select_user()
    if client is None:
        exit()
    client.prompt_edit_user()
    print(client.card())

if args.new_invoice:
    client = Client.Client.prompt_select_user()
    if client is None:
        exit()
    invoice = Invoice.Invoice()
    invoice.prompt_new_invoice(client)

if args.list_invoice:
    for client in Client.Client.clients_iter():
        print()
        print(client.card())
        client.load_invoices()
        for invoice in client.invoices:
            
            print(f"  - {invoice}")
    pass

if args.list_active_invoice:
    pass




# readline.insert_text('test')
# readline.redisplay()
# time.sleep(1)
# print(readline.get_line_buffer())
# print(input(">"))