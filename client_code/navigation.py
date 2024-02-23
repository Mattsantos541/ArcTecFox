from ..vault import vault
from ..homeanon import homeanon
from ..account import account
from ..datagen import datagen
from ..scorecard import scorecard
from ..homedetails import homedetails

__home = None
def get_form():
  if __home is None:
    raise Exception("You must set home form first.")

return __home
def go_vault():
  form = get_form()
  form.load_component(vault())


def go_home():
  form = get_form()
  form.load_component(homeanon())

def go_datagen():
  form = get_form()
  form.load_component(datagen())

def got_scorecard():
  form = get_form()
  form.load_component(scorecard())

def go_account():
  form = get_form()
  form.load_component(account())
