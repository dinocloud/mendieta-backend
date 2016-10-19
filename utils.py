import random
import string
from model import *
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

def random_string(length=20):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


