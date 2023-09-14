import random
import string

def generatePassword(lenght):
    return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(lenght)])