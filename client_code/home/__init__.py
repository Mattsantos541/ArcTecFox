from ._anvil_designer import homeTemplate
from anvil import *
from ..register import register

class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_home_click(self, **event_args):
      cmpt= 
     # Load Form1 into the ContentPanel
      self.content_panel.clear()  # Clear existing content
      self.content_panel.add_component(cmpt)