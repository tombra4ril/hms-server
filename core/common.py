"""
  Contains utility functions
"""
from datetime import datetime, timedelta
from decouple import config
import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent

def get_category():
  """
    Reads in and return the categories to be stored in the database
  """
  return json.loads(open(base_dir / "initial_users.json").read())

def get_category_names():
  """
    Returns only the names of all the category
  """
  json_object = json.loads(open(base_dir / "initial_users.json").read())
  return json_object["names"]

def get_category_initials():
  """
    Returns only the initials of all the category
  """
  json_object = json.loads(open(base_dir / "initial_users.json").read())
  return json_object["initials"]

def get_category_name_from_initials(name=""):
  """
    Returns a initial from the name passed as argument
    ______________________________________
    name: Required - This is the only argument supplied to return the initials
  """
  index = None
  name = name.lower()
  if(name == ""):
    return index
  else:
    names = get_category_names()
    for _, __ in enumerate(names):
      if(__.lower() == name):
        index = _
        break
    return get_category_initials()[index]

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
