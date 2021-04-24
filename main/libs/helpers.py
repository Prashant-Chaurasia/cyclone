import random, string
from datetime import datetime


def random_word(length):
   alpha_numerals = string.ascii_letters + string.digits
   return ''.join(random.choice(alpha_numerals) for i in range(length))

def generate_id(prefix):
    return f'{prefix}{random_word(10)}'

def parse_datetime(str_dt):
	return datetime.strptime(str_dt, '%Y-%m-%d %H:%M')
