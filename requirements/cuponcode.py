import random
def get_promo_code():
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, 5):
         slice_start = random.randint(0, len(code_chars) - 1)
         code += code_chars[slice_start: slice_start + 1]
    return code

obj = get_promo_code()
print(obj)
