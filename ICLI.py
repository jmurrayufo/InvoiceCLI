#!/usr/bin/env python3

import readline
import time
import argparse


from code import Client


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

args = parser.parse_args()
print(args)

if args.add_client:
    x = Client.Client()
    x.prompt_edit_user()

if args.edit_client:
    x = Client.Client.prompt_select_user()
    x.prompt_edit_user()
    print(x.user_card())


# readline.insert_text('test')
# readline.redisplay()
# time.sleep(1)
# print(readline.get_line_buffer())
# print(input(">"))