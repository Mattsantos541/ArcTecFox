from ._anvil_designer import homedetailsTemplate
from anvil import *

class homedetails(homedetailsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
