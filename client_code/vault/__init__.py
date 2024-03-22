from ._anvil_designer import vaultTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class vault(vaultTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  # Check if a user is logged in
    if anvil.server.call('check_user'):
    # If the user is logged in, proceed to fetch and display datasets
      user_datasets = anvil.server.call('get_user_datasets')
      self.repeating_panel_1.items = user_datasets
    else:
        # Handle the scenario where no user is logged in
      print("No user is logged in.")
        # Here you could display a notification or redirect to a login form
        # For example, using Notification:
      from anvil import Notification
      Notification("Please log in to view datasets.", timeout=3).show()
