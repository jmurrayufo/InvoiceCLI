#!/usr/bin/env python3

import readline
import time

from code import Client

x = Client.Client()
x.prompt_edit_user()
print(x)

# readline.insert_text('test')
# readline.redisplay()
# time.sleep(1)
# print(readline.get_line_buffer())
# print(input(">"))