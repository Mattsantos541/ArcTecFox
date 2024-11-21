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

        # Explicitly set event handler for the preview button
        self.button_preview.set_event_handler('click', self.button_preview_click)

    def fetch_vault_datasets(self):
        """Load datasets from the Vault and populate the dropdown."""
        try:
            print("Fetching datasets from Vault...")  # Debugging print
            # Calls the server function to get datasets for the current user
            datasets = anvil.server.call('get_user_vault_datasets')  
            if datasets:
                # Populate the dropdown with dataset names and their IDs
                self.vault_datasets_dropdown.items = [(row['dataset_name'], row.get_id()) for row in datasets]
                self.vault_datasets_dropdown.enabled = True  # Enable the dropdown after loading items
                print(f"Loaded datasets: {[item[0] for item in self.vault_datasets_dropdown.items]}")  # Debugging
            else:
                print("No datasets found.")  # Debugging
        except Exception as e:
            print(f"Error loading datasets: {str(e)}")  # Debugging
            alert(f"Error loading datasets: {str(e)}")

    def vault_datasets_dropdown_change(self, **event_args):
        """When a Vault dataset is selected, display its name and enable the preview button."""
        try:
            selected_dataset_id = self.vault_datasets_dropdown.selected_value
            if selected_dataset_id:
                # Find the selected dataset name
                selected_dataset_name = [item[0] for item in self.vault_datasets_dropdown.items if item[1] == selected_dataset_id][0]
                print(f"Selected dataset ID: {selected_dataset_id}")  # Debugging
                print(f"Selected dataset name: {selected_dataset_name}")  # Debugging

                # Update UI with selected dataset name
                self.text_box_file_name.text = f"Vault Dataset: {selected_dataset_name}"
                # Enable preview button after a dataset is selected
                self.button_preview.enabled = True
            else:
                print("No dataset selected.")  # Debugging
        except Exception as e:
            print(f"Error handling dropdown change: {str(e)}")  # Debugging
            alert(f"Error handling dropdown change: {str(e)}")

    def file_loader_dataset_change(self, **event_args):
        """Triggered when a file is uploaded."""
        try:
            file = self.file_loader_dataset.file
            if file:
                self.text_box_file_name.text = f"Uploaded Dataset: {file.name}"
                self.button_preview.enabled = True
                print(f"File uploaded: {file.name}")  # Debugging
            else:
                print("No file uploaded.")  # Debugging
        except Exception as e:
            print(f"Error handling file upload: {str(e)}")  # Debugging
            alert(f"Error handling file upload: {str(e)}")

    def button_preview_click(self, **event_args):
        """Preview the selected or uploaded dataset."""
        try:
            print("Preview button clicked.")  # Debugging
            selected_dataset_id = self.vault_datasets_dropdown.selected_value
            file = self.file_loader_dataset.file

            # Fetch preview data from the server
            if file:
                print("Generating preview for uploaded file...")  # Debugging
                describe_output, preview_rows = anvil.server.call('generate_preview', file)
            elif selected_dataset_id:
                print(f"Generating preview for selected dataset ID: {selected_dataset_id}")  # Debugging
                describe_output, preview_rows = anvil.server.call('preview_dataset', selected_dataset_id)
            else:
                alert("Please upload a file or select a dataset from the Vault.")
                print("No file or dataset selected for preview.")  # Debugging
                return

            # Display .describe() output in the text area
            self.text_area_info.text = describe_output

            # Set up columns in the DataGrid dynamically based on the preview rows
            if preview_rows:
                print("Setting up DataGrid with preview rows.")  # Debugging
                self.data_grid_preview.columns = []  # Clear existing columns
                for key in preview_rows[0].keys():
                    self.data_grid_preview.columns.append({
                        'id': key,
                        'title': key,
                        'data_key': key
                    })
                self.data_grid_preview.items = preview_rows  # Set items in DataGrid
            else:
                alert("No preview rows available.")
                print("Preview rows are empty.")  # Debugging
        except Exception as e:
            print(f"Error generating preview: {str(e)}")  # Debugging
            alert(f"Error generating preview: {str(e)}")
