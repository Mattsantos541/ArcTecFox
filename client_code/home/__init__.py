from ._anvil_designer import homeTemplate
from anvil import *
from ..vault import vault
from ..homeanon import homeanon
from ..account import account
from ..datagen import datagen
from ..scorecard import scorecard
from ..


class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_vault_click(self, **event_args):
    self.link_vault.role = 'selected'
    self.load_component(vault())


  def link_home_click(self, **event_args):
    self.load_component(homeanon())

  def link_datagen_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_scorecard_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_account_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_signin_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_logout_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def load_component(self, cmpt):
    self.column_panel_content.clear()
    self.column_panel_content.add_component(cmpt)
