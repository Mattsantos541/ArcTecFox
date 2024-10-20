# In datagen.py

from ._anvil_designer import datagenTemplate  # Ensure this matches the auto-generated template class
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .. import navigation  # Assuming you're using a navigation module


class datagen(datagenTemplate):
    def __init__(self, **properties):
        print("Datagen form initialized")
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Disable the preview button and dropdown initially
        self.button_preview.enabled = False
        self.dropdown_vault_datasets.enabled = False

        # Load datasets from the Vault on form load
        self.load_vault_datasets()

    def load_vault_datasets(self):
        """Load datasets from the Vault and populate the dropdown"""
        try:
            datasets = anvil.server.call('get_vault_datasets')  # Call server to get datasets
            if datasets:
                self.dropdown_vault_datasets.items = [(row['dataset_name'], row['id']) for row in datasets]
                self.dropdown_vault_datasets.enabled = True  # Enable dropdown if datasets are available
        except Exception as e:
            alert(f"Error loading datasets: {str(e)}")  # Show error if dataset loading fails

    def dropdown_vault_datasets_change(self, **event_args):
        """When a Vault dataset is selected, display its name and enable the preview button"""
        selected_dataset_name = self.dropdown_vault_datasets.selected_value
        if selected_dataset_name:
            self.text_box_file_name.text = f"Vault Dataset: {selected_dataset_name}"
            self.button_preview.enabled = True  # Enable preview button once a dataset is selected

    def file_loader_dataset_change(self, **event_args):
        """Triggered when a file is uploaded"""
        file = self.file_loader_dataset.file
        if file:
            self.text_box_file_name.text = f"Uploaded Dataset: {file.name}"
            self.button_preview.enabled = True  # Enable preview button after a file is uploaded

    def button_preview_click(self, **event_args):
        """Preview the selected or uploaded dataset"""
        # Check if a file was uploaded or a Vault dataset was selected
        file = self.file_loader_dataset.file
        selected_dataset_id = self.dropdown_vault_datasets.selected_value
        
        try:
            if file:
                # If a file was uploaded, generate a preview
                preview_info, preview_rows = anvil.server.call('generate_preview', file)
            elif selected_dataset_id:
                # If a Vault dataset was selected, generate a preview for it
                preview_info, preview_rows = anvil.server.call('preview_vault_dataset', selected_dataset_id)
            else:
                alert("Please upload a file or select a dataset from the Vault.")
                return

            # Display the dataset preview information
            self.text_area_info.text = preview_info  # Show pandas info
            self.data_grid_preview.items = preview_rows  # Show first few rows of the dataset

        except Exception as e:
            alert(f"Error generating preview: {str(e)}")  # Show error message if preview fails