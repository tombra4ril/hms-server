"""
  Contains utility functions
"""
from datetime import datetime, timedelta
from decouple import config

def token_time(time, type="", add=0):
  """ Computes timedelta depending on the type(access token or refresh token) and time (in seconds, minutes or hours)
  
    time: Is a str which is seconds, minutes or hours
    
    type: Is a str which can either be ACCESS or REFRESH
    
    add: Is an int, if present will make this function return a timedelta set the time parameter to the parameter passed as add
  """
  if(time == "seconds"):
    if add == 0:
      return timedelta(seconds=config(f"{type}_TOKEN_EXPIRES_IN", default="3600", cast=int))
    else:
      return datetime.now() + timedelta(seconds=add)
  elif(time == "minutes"):
    if add == 0:
      return timedelta(minutes=config(f"{type}_EXPIRES_IN", default="15", cast=int))
    else:
      return datetime.now() + timedelta(minutes=add)
  else:
    if add == 0:
      return timedelta(hours=config(f"{type}_EXPIRES_IN", default="3", cast=int))
    else:
      return datetime.now() + timedelta(hours=add)