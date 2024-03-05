import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

from vault import vault
from homeanon import homeanon
from account import account
from datagen import datagen
from scorecard import scorecard
from homedetails import homedetails
from .signup import signup

home = None
def get_form():
  if home is None:
    raise Exception("You must set home form first.")

  return home
def go_vault():
  set_active_nav('vault')
  set_title("Vault")
  form = get_form()
  form.load_component(vault())


def go_home():
  set_active_nav('home')
  set_title('')
  form = get_form()
  form.load_component(homeanon())

def go_datagen():
  set_active_nav('datagen')
  set_title('DataGen')
  form = get_form()
  form.load_component(datagen())

def go_scorecard():
  set_active_nav('scorecard')
  set_title("Scorecard")
  form = get_form()
  form.load_component(scorecard())

def go_account():
  set_active_nav('account')
  set_title('Account')
  form = get_form()
  form.load_component(account())

def go_signup():
  set_active_nav('signup')
  set_title("signup")
  form = get_form()
  form.load_component(signup())

def set_title(text):
  form = get_form()
  base_title = form.base_title
  if text:
    form.headline_1.text = base_title + ": " + text  
  else:
    form.headline_1.text = base_title
def set_active_nav(state):
  form = get_form()
  form.set_active_nav(state)
  
