from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.tables as tables
from anvil.tables import app_tables

class RowTemplate4(RowTemplate4Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def button_delete_click(self, **event_args):
        """Triggered when the delete button is clicked in a dataset row."""
        # Access the dataset row associated with this row in the Data Grid
        dataset_row = self.item
        dataset_name = dataset_row['dataset_name']

        # Confirm deletion with the user
        confirm_delete = confirm(f"Are you sure you want to delete the dataset '{dataset_name}'?")
        if confirm_delete:
            # Delete the dataset from the database if confirmed
            dataset_row.delete()
            
            # Trigger an event to refresh the Data Grid in the Vault form
            self.parent.raise_event('x-refresh-datasets')

            # Show a confirmation alert
            alert(f"'{dataset_name}' has been deleted.", title="Dataset Deleted")
