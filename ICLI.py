#!/usr/bin/env python3

import readline
import time
import argparse


from code import Client, Invoice


parser = argparse.ArgumentParser(
    description="Invoice Command Line Interface",
    )

subparsers = parser.add_subparsers(
    help="Sub command help",
    dest='cmd')

client_parser = subparsers.add_parser(
    "client",
    help="Client manipulations")
client_parser.add_argument(
    "sub_cmd",
    choices=['new','edit','list'])

invoice_parser = subparsers.add_parser(
    "invoice",
    help="Invoice manipulations")
invoice_parser.add_argument(
    "sub_cmd")

args = parser.parse_args()
print(args)

if args.cmd == 'client':
    if args.sub_cmd == 'new':
        client = Client.Client()
        client.prompt_edit_user()
    elif  args.sub_cmd == 'edit':
        client = Client.Client.prompt_select_user()
        if client is None:
            exit()
        client.prompt_edit_user()
        print(client.card())
    elif  args.sub_cmd == 'list':
        for client in Client.Client.clients_iter():
            print()
            print(client.card())

if args.cmd == 'invoice':    
    if args.sub_cmd == 'new':
        client = Client.Client.prompt_select_user()
        if client is None:
            exit()
        invoice = Invoice.Invoice()
        invoice.prompt_new_invoice(client)
    elif args.sub_cmd == 'list':
        for client in Client.Client.clients_iter():
            print()
            print(client.card())
            client.load_invoices()
            for invoice in client.invoices:
                print(f"  - {invoice}")    
    elif args.sub_cmd == 'list-active':
        raise NotImplementedError("Can't list active yet.")






# readline.insert_text('test')
# readline.redisplay()
# time.sleep(1)
# print(readline.get_line_buffer())
# print(input(">"))