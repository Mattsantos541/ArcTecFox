from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ..import navigation



class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.base_title = self.headline_1.text
    navigation.home = self
    navigation.go_home()

  def link_account_click(self, **event_args):
    navigation.go_account()

  def link_home_click(self, **event_args):
    navigation.go_home()

  def link_vault_click(self, **event_args):
    navigation.go_vault()

  def link_datagen_click(self, **event_args):
    navigation.go_datagen()

  def link_scorecard_click(self, **event_args):
    navigation.go_scorecard()
    

  def link_register_click(self, **event_args):
    anvil.users.signup_with_form(allow_cancel=True)  

  def link_signin_click(self, **event_args):
    anvil.users.login_with_email(remember=False)

  def link_logout_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def load_component(self, cmpt):
    self.column_panel_content.clear()
    self.column_panel_content.add_component(cmpt)

  def set_active_nav(self, state):
    self.link_home.role = 'selected' if state == 'home' else None
    self.link_vault.role = 'selected' if state == 'vault' else None
    self.link_datagen.role = 'selected' if state == 'datagen' else None
    self.link_scorecard.role = 'selected' if state == 'scorecard' else None


    


