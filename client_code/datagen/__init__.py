from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ._anvil_designer import DatagenForm

from ..import navigation
from .. import datasets_server


class DatagenForm(DatagenFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Disable the preview button initially
        self.button_preview.enabled = False

        # Load datasets from the Vault on form load
        self.load_vault_datasets()

    def load_vault_datasets(self):
        """Load datasets from the Vault and populate the dropdown"""
        datasets = anvil.server.call('get_vault_datasets')
        self.dropdown_vault_datasets.items = [(row['dataset_name'], row['id']) for row in datasets]

        if datasets:
            self.dropdown_vault_datasets.enabled = True

    def dropdown_vault_datasets_change(self, **event_args):
        """When a Vault dataset is selected, display its name and enable the preview button"""
        selected_dataset_name = self.dropdown_vault_datasets.selected_value
        if selected_dataset_name:
            self.text_box_file_name.text = f"Vault Dataset: {self.dropdown_vault_datasets.selected_value}"
            self.button_preview.enabled = True

    def file_loader_dataset_change(self, **event_args):
        """Triggered when a file is uploaded"""
        file = self.file_loader_dataset.file
        if file:
            self.text_box_file_name.text = f"Uploaded Dataset: {file.name}"
            self.button_preview.enabled = True

    def button_preview_click(self, **event_args):
        """Preview the selected or uploaded dataset"""
        # Check if a file was uploaded or a Vault dataset was selected
        file = self.file_loader_dataset.file
        selected_dataset_id = self.dropdown_vault_datasets.selected_value
        
        if file:
            # If a file was uploaded, preview it
            preview_info, preview_rows = anvil.server.call('generate_preview', file)
        elif selected_dataset_id:
            # If a Vault dataset was selected, preview it
            preview_info, preview_rows = anvil.server.call('preview_vault_dataset', selected_dataset_id)

        # Display the preview info and rows
        self.text_area_info.text = preview_info
        self.data_grid_preview.items = preview_rows

