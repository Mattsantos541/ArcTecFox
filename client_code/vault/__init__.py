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

    

  def button_upload_click(self, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if self.file_loader_1.file and self.text_box_datasetdesc.text:
      # Call server function to upload and process dataset
      result = anvil.server.call('upload_dataset',
                                self.file_loader_1.file,
                                self.text_box_datasetdesc.text)
      if result == "success":
        Notification("Dataset uploaded successfully.", timeout=3).show()
        # Optionally, refresh the datsets list or take other actions
      else:
        Notification("Failed to upload dataset.", timeout=3).show()
    else:
      Notification("Please select a file and enter a file description", timeout=3).show()

def file_loader_1_change(self, **event_args):
    """This method is called when the file is uploaded."""
    file = self.file_loader_1.file
    if file:
        # Handle the file upload logic here
        print(f"File uploaded: {file.name}")

