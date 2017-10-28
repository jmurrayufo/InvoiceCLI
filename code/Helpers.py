

def prompt_text(prompt):
    while 1:
        try:
            ret_val = input(prompt)
            if ret_val == '':
                return None
            return ret_val
        except:
            raise


def prompt_float(prompt):
    while 1:
        try:
            ret_val = input(prompt)
            if ret_val == '':
                return None
            return float(ret_val)
        except ValueError:
            print("Value must be a valid float")


def prompt_valid_index(prompt, _range=None):
    while 1:
        try:
            ret_val = input(prompt)
            if ret_val == '':
                return None
            ret_val = int(ret_val)
            if _range is not None and ret_val not in _range:
                print("Selection not in range!")
                continue
            return ret_val
        except:
            raise