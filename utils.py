import random

def convert_obj(obj):
  try:
    return float(obj.replace('..', '').replace(',', ''))
  except AttributeError:
    return float(obj)

def rand_agent(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)