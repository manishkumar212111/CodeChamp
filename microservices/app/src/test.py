

from random import randint
import string
import random
def id_generator(size=11, chars=string.ascii_uppercase+string.ascii_lowercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))
print randint(6,12)
print id_generator()




