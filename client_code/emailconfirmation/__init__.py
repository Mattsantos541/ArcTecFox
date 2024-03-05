from ._anvil_designer import emailconfirmationTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class emailconfirmation(emailconfirmationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    try:
        anvil.server.call('confirm_email', token)
            # Show a confirmation message or redirect to the login page
            open_form('Form_Login')
      except Exception as e:
            # Handle the error, e.g., show a message to the user
            pass

    # Any code you write here will run before the form opens.
