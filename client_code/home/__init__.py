from ._anvil_designer import homeTemplate
from anvil import *
from ..vault import vault

class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_vault_click(self, **event_args):
    cmpt = vault()
    self.link_vault.role = 'selected'

    self.column_panel_content.clear()
    self.column_panel_content.add_component(cmpt)

