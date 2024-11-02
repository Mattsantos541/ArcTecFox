from ._anvil_designer import datagenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.users
from .. import navigation

class datagen(datagenTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings
        self.init_components(**properties)
        print("Datagen form initialized")  # Debugging print
        
        # Disable the preview button and dropdown initially
        self.button_preview.enabled = False
        self.vault_datasets_dropdown.enabled = False  # Ensure this matches the component name in the IDE

        # Load datasets from the Vault on form load
        self.fetch_vault_datasets()

    def fetch_vault_datasets(self):
        """Load datasets from the Vault and populate the dropdown."""
        try:
            # Calls the server function to get datasets for the current user
            datasets = anvil.server.call('get_user_vault_datasets')  
            if datasets:
                # Populate the dropdown with dataset names and their IDs
                self.vault_datasets_dropdown.items = [(row['dataset_name'], row['id']) for row in datasets]
                self.vault_datasets_dropdown.enabled = True  # Enable the dropdown after loading items
        except Exception as e:
            alert(f"Error loading datasets: {str(e)}")

    def vault_datasets_dropdown_change(self, **event_args):
        """When a Vault dataset is selected, display its name and enable the preview button."""
        selected_dataset_id = self.vault_datasets_dropdown.selected_value
        if selected_dataset_id:
            # Find the selected dataset name
            selected_dataset_name = [item[0] for item in self.vault_datasets_dropdown.items if item[1] == selected_dataset_id][0]
            print(f"Selected dataset ID: {selected_dataset_id}")  # Debugging: print selected dataset ID
            print(f"Selected dataset name: {selected_dataset_name}")  # Debugging: print selected dataset name

            # Update UI with selected dataset name
            self.text_box_file_name.text = f"Vault Dataset: {selected_dataset_name}"
            # Enable preview button after a dataset is selected
            self.button_preview.enabled = True

    def file_loader_dataset_change(self, **event_args):
        """Triggered when a file is uploaded."""
        file = self.file_loader_dataset.file
        if file:
            self.text_box_file_name.text = f"Uploaded Dataset: {file.name}"
            self.button_preview.enabled = True

    def button_preview_click(self, **event_args):
        """Preview the selected or uploaded dataset."""
        # Check if a Vault dataset is selected or a file is uploaded
        selected_dataset_id = self.vault_datasets_dropdown.selected_value
        file = self.file_loader_dataset.file
        
        try:
            if file:
                # Generate preview for the uploaded file
                preview_info, preview_rows = anvil.server.call('generate_preview', file)
            elif selected_dataset_id:
                # Generate preview for the selected vault dataset
                preview_info, preview_rows = anvil.server.call('preview_dataset', selected_dataset_id)
            else:
                alert("Please upload a file or select a dataset from the Vault.")
                return

            # Display the preview information
            self.text_area_info.text = preview_info  # Show pandas info
            self.data_grid_preview.items = preview_rows  # Show first few rows of the dataset
        except Exception as e:
            alert(f"Error generating preview: {str(e)}")


def vault_datasets_dropdown_change(self, **event_args):
    """When a Vault dataset is selected, display its name and enable the preview button."""
    selected_dataset_id = self.vault_datasets_dropdown.selected_value
    if selected_dataset_id:
        # Find the selected dataset name
        selected_dataset_name = [item[0] for item in self.vault_datasets_dropdown.items if item[1] == selected_dataset_id][0]
        print(f"Selected dataset ID: {selected_dataset_id}")  # Debugging: print selected dataset ID
        print(f"Selected dataset name: {selected_dataset_name}")  # Debugging: print selected dataset name

        # Update UI with selected dataset name
        self.text_box_file_name.text = f"Vault Dataset: {selected_dataset_name}"
        # Enable preview button after a dataset is selected
        self.button_preview.enabled = True

