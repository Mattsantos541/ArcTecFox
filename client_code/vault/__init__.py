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

    # Fetch the currently logged-in user
    user = anvil.users.get_user()
    print("Debug - Logged in user:", user['email'] if user else "No user logged in")

    # Any code you write here will run before the form opens.

    datasets = app_tables.datasets.search(user=user)
    print(f"Debug - Number of datasets found: {len(datasets)}")

    # Prepare the data for the Repeating Panel
    prepared_data = [{'dataset_name': row['dataset_name'],
                      'upload_date': row['upload_date'],
                      'Size': row['size'],
                      'desc': row['desc'],
                      'fulldataset': row['fulldataset']
                      # Add any other fields you want to display
                     } for row in datasets]
    print("Debug - Prepared data:", prepared_data)
    self.repeating_panel_1.items = prepared_data
