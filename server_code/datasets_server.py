import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import io

@anvil.server.callable
def get_user_vault_datasets():
    """Fetch datasets for the currently logged-in user"""
    user = anvil.users.get_user()
    if not user:
        raise Exception("No user is logged in")
    
    # Return datasets where the user is the owner
    return app_tables.datasets.search(user=user)

@anvil.server.callable
def generate_preview(file):
    """Generate a preview of the dataset."""
    try:
        # Determine the file type and read it into a DataFrame
        if file.content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/json':
            df = pd.read_json(io.BytesIO(file.get_bytes()))
        else:
            return "Unsupported file type.", []

        # Generate `.describe()` output as a string
        describe_output = df.describe(include='all').to_string()

        # Get the first five rows for the DataGrid
        preview_rows = df.head().to_dict(orient='records')

        return describe_output, preview_rows
    except Exception as e:
        print(f"Error generating preview: {str(e)}")
        return f"Error generating preview: {str(e)}", []

@anvil.server.callable
def preview_dataset(dataset_id):
    """Generates a preview of the dataset stored in the Vault by dataset ID."""
    dataset_row = app_tables.datasets.get_by_id(dataset_id)
    if not dataset_row:
        return "Dataset not found.", []

    file = dataset_row['fulldataset']
    if not file:
        return "No file found in this dataset.", []

    # Reuse the generate_preview function for processing
    return generate_preview(file)
