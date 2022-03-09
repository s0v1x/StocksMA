def convert_obj(obj):
  try:
    return float(obj.replace('..', '').replace(',', ''))
  except AttributeError:
    return float(obj)