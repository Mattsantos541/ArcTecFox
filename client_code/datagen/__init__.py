from ._anvil_designer import datagenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

class datagen(datagenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Disable preview button initially
    self.button_preview.enabled = False
        
    # Load datasets from the Vault
    self.load_vault_datasets()



  #on generate button click, show loading bar and on completion go to scorecard page

def load_vault_datasets(self, **event_args):
    """Load datasets from the Vault and populate the dropdown."""
    # Call server function to get the list of datasets
    datasets = anvil.server.call('get_vault_datasets')
    
    # Populate the dropdown with dataset names and their IDs
    self.dropdown_vault_datasets.items = [(row['dataset_name'], row['id']) for row in datasets]
    
    # Enable the dropdown if datasets are found
    if datasets:
        self.dropdown_vault_datasets.enabled = True
    else:
        self.dropdown_vault_datasets.enabled = False  # Disable dropdown if no datasets are found
