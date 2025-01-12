from ._anvil_designer import vaultTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.users
from anvil.tables import app_tables

class vault(vaultTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Load datasets when the form opens
        self.load_datasets()
        
        # Set up an event handler for refreshing the dataset list after deletion
        self.repeating_panel_1.set_event_handler('x-refresh-datasets', self.load_datasets)



    def button_upload_click(self, **event_args):
        """Triggered when a new file and description are provided."""
        if self.file_loader_1.file and self.text_box_datasetdesc.text:
            # Call server function to upload and process dataset
            result = anvil.server.call('upload_dataset',
                                       self.file_loader_1.file,
                                       self.text_box_datasetdesc.text)
            if result == "success":
                Notification("Dataset uploaded successfully.", timeout=3).show()
                self.load_datasets()  # Refresh the dataset list
            else:
                Notification("Failed to upload dataset.", timeout=3).show()
        else:
            Notification("Please select a file and enter a dataset description.", timeout=3).show()

    def file_loader_1_change(self, **event_args):
        """This method is called when the file is uploaded."""
        file = self.file_loader_1.file
        if file:
            print(f"File uploaded: {file.name}")

    def load_datasets(self, **event_args):
        """Fetch and display datasets for the current user."""
        datasets = anvil.server.call('get_user_vault_datasets')
        self.repeating_panel_1.items = datasets

    def button_preview_click(self, **event_args):
        """Preview the selected dataset"""
        dataset_id = self.selected_dataset_id  # Replace with the actual selection mechanism

        if dataset_id:
            preview_info, preview_rows = anvil.server.call('preview_dataset', dataset_id)
            self.text_area_info.text = preview_info
            self.data_grid_preview.items = preview_rows
        else:
            alert("Please select a dataset to preview.")
