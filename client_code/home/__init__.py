from ._anvil_designer import homeTemplate
from anvil import *

class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_register_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('register')

  def link_dash_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_dg_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_scorecard_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_login_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_account_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_logout_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass
