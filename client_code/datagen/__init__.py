from ._anvil_designer import datagenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .. import navigation

class datagen(datagenTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        print("Datagen form initialized")  # Debugging print
        
        # Disable the preview button and dropdown initially
        self.button_preview.enabled = False
        self.vault_datasets_dropdown.enabled = False  # Ensure this matches the component name in the IDE

        # Load datasets from the Vault on form load
        self.fetch_vault_datasets()

    def fetch_vault_datasets(self):
        """Load datasets from the Vault and populate the dropdown"""
        try:
            datasets = anvil.server.call('fetch_vault_datasets')  # Calling server function
            if datasets:
                # Populate dropdown with dataset names and IDs
                self.vault_datasets_dropdown.items = [(row['dataset_name'], row['id']) for row in datasets]
                self.vault_datasets_dropdown.enabled = True  # Enable dropdown when data is loaded
        except Exception as e:
            alert(f"Error loading datasets: {str(e)}")

    def vault_datasets_dropdown_change(self, **event_args):
        """When a Vault dataset is selected, display its name and enable the preview button"""
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
        """Triggered when a file is uploaded"""
        file = self.file_loader_dataset.file
        if file:
            self.text_box_file_name.text = f"Uploaded Dataset: {file.name}"
            self.button_preview.enabled = True

    def button_preview_click(self, **event_args):
        """Preview the selected or uploaded dataset"""
        dataset_id = self.vault_datasets_dropdown.selected_value  # Use the selected value from the dropdown

        if dataset_id:
            # Fetch preview info and rows from the server
            preview_info, preview_rows = anvil.server.call('preview_dataset', dataset_id)
            self.text_area_info.text = preview_info  # Display dataset info
            self.data_grid_preview.items = preview_rows  # Display first few rows
        else:
            alert("Please select a dataset to preview.")
