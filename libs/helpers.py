import random, string

def random_word(length):
   alpha_numerals = string.ascii_letters + string.digits
   return ''.join(random.choice(alpha_numerals) for i in range(length))

def generate_id(prefix):
    return f'{prefix}{random_word(10)}'
