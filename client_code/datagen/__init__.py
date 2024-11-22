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
        print("Datagen form initialized.")  # Debugging print
        
        # Disable the preview button and dropdown initially
        self.button_preview.enabled = False
        self.vault_datasets_dropdown.enabled = False

        # Load datasets from the Vault on form load
        self.fetch_vault_datasets()

        # Explicitly set the event handler for the preview button
        self.button_preview.set_event_handler('click', self.button_preview_click)

    def fetch_vault_datasets(self):
        """Load datasets from the Vault and populate the dropdown."""
        try:
            print("Fetching datasets from Vault...")
            datasets = anvil.server.call('get_user_vault_datasets')
            if datasets:
                self.vault_datasets_dropdown.items = [(row['dataset_name'], row.get_id()) for row in datasets]
                self.vault_datasets_dropdown.enabled = True
                print(f"Loaded datasets: {[item[0] for item in self.vault_datasets_dropdown.items]}")
            else:
                print("No datasets found.")
        except Exception as e:
            print(f"Error loading datasets: {str(e)}")
            alert(f"Error loading datasets: {str(e)}")

    def vault_datasets_dropdown_change(self, **event_args):
        """Triggered when the dropdown selection changes."""
        try:
            selected_dataset_id = self.vault_datasets_dropdown.selected_value
            if selected_dataset_id:
                # Extract dataset name
                selected_dataset_name = [
                    item[0] for item in self.vault_datasets_dropdown.items if item[1] == selected_dataset_id
                ][0]
                self.text_box_file_name.text = f"Selected Dataset: {selected_dataset_name}"
                self.button_preview.enabled = True
                print(f"Dataset selected: {selected_dataset_name}")
            else:
                print("No dataset selected.")
        except Exception as e:
            print(f"Error handling dropdown change: {e}")
            alert(f"Error handling dropdown change: {e}")

    def file_loader_dataset_change(self, **event_args):
        """Triggered when a file is uploaded."""
        try:
            file = self.file_loader_dataset.file
            if file:
                self.text_box_file_name.text = f"Uploaded Dataset: {file.name}"
                self.button_preview.enabled = True
                print(f"File uploaded: {file.name}")
            else:
                print("No file uploaded.")
        except Exception as e:
            print(f"Error handling file upload: {e}")
            alert(f"Error handling file upload: {e}")

    def button_preview_click(self, **event_args):
        """Preview the selected or uploaded dataset."""
        try:
            print("Preview button clicked.")
            selected_dataset_id = self.vault_datasets_dropdown.selected_value
            file = self.file_loader_dataset.file

            if file:
                print("Generating preview for uploaded file...")
                describe_output, preview_rows = anvil.server.call('generate_preview', file)
            elif selected_dataset_id:
                print(f"Generating preview for selected dataset ID: {selected_dataset_id}")
                describe_output, preview_rows = anvil.server.call('preview_dataset', selected_dataset_id)
            else:
                alert("Please upload a file or select a dataset.")
                print("No file or dataset selected for preview.")
                return

            # Display describe output in the text area
            self.text_area_info.text = describe_output

            # Dynamically configure and populate the DataGrid
            if preview_rows:
                print(f"Preview Rows: {preview_rows}")
                self.data_grid_preview.columns = []
                for col_name in preview_rows[0].keys():
                    self.data_grid_preview.columns.append({
                        'id': col_name,
                        'title': col_name,
                        'data_key': col_name
                    })
                self.data_grid_preview.items = preview_rows
                print("DataGrid populated successfully.")
            else:
                alert("No data available for preview.")
                print("Preview rows are empty.")
        except Exception as e:
            print(f"Error generating preview: {str(e)}")
            alert(f"Error generating preview: {str(e)}")

