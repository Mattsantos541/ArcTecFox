from ._anvil_designer import homeTemplate
from anvil import *
from ..import navigation



class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  # at loading iof the app
    



  def link_signin_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_logout_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def load_component(self, cmpt):
    self.column_panel_content.clear()
    self.column_panel_content.add_component(cmpt)
