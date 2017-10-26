

def prompt_text(prompt):
    while 1:
        try:
            ret_val = input(prompt)
            return ret_val
        except:
            raise