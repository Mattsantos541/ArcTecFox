from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .. import navigation  # Ensure this import statement is correct


class home(homeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    user = anvil.users.get_user()
    print("[__init__] Current user:", user)
    self.update_welcome_message(user)


    navigation.home = self
    navigation.go_home()



    def update_welcome_message(self, user):
      print("[update_welcome_message] User object:", user)
      if user:
        email = user['email']
        print("[update_welcome_message] Setting welcome message for:", email)
        self.link_account.text = f"Welcome {email}"
      else:
        print("[update_welcome_message] No user logged in, setting as guest.")
        self.link_account.text = "Welcome Guest"

    print("Before email update, user:", anvil.users.get_user()['email'])
    # Code to update user's email
    print("After email update, user:", anvil.users.get_user()['email'])



    def form_show(self, **event_args):
      user = anvil.users.get_user()
      print("[form_show] Showing form to user:", user)
      self.update_welcome_message(user)



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
        user = anvil.users.signup_with_form(allow_cancel=True)
        self.set_account_state(user)
        navigation.go_vault()

    def link_login_click(self, **event_args):
        user = anvil.users.login_with_form(allow_cancel=True)
        self.set_account_state(user)
        navigation.go_vault()

    def link_logout_click(self, **event_args):
        anvil.users.logout()
        self.set_account_state(None)
        navigation.go_home()

    def load_component(self, cmpt):
        self.column_panel_content.clear()
        self.column_panel_content.add_component(cmpt)

    def set_active_nav(self, state):
        self.link_home.role = 'selected' if state == 'home' else None
        self.link_vault.role = 'selected' if state == 'vault' else None
        self.link_datagen.role = 'selected' if state == 'datagen' else None
        self.link_scorecard.role = 'selected' if state == 'scorecard' else None

    def set_account_state(self, user):
        self.link_account.visible = user is not None
        self.link_logout.visible = user is not None
        self.link_login.visible = user is None
        self.link_register.visible = user is None
