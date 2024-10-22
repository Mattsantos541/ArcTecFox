import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import io


@anvil.server.callable
def get_vault_datasets():
    """Fetch datasets stored in the Vault"""
    return app_tables.datasets.search()

@anvil.server.callable
def preview_vault_dataset(dataset_id):
    """Preview the dataset stored in the Vault"""
    dataset = app_tables.datasets.get_by_id(dataset_id)
    file = dataset['fulldataset']  # Assuming 'fulldataset' is the column storing the file
    
    return generate_preview(file)

@anvil.server.callable
def generate_preview(file):
    """Generate a preview of the dataset"""
    try:
        if file.content_type == 'text/csv':
            df = pd.read_csv(file.get_bytes_io())
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file.get_bytes_io())
        elif file.content_type == 'application/json':
            df = pd.read_json(file.get_bytes_io())
        else:
            return "Unsupported file type.", []

        # Generate pandas info
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_output = buffer.getvalue()

        # Preview the first 5 rows of the dataset
        preview_rows = df.head().to_dict(orient='records')
        return info_output, preview_rows
    except Exception as e:
        return f"Error generating preview: {str(e)}", []

@anvil.server.callable
def get_user_vault_datasets():
    """Fetch datasets for the currently logged-in user"""
    user = anvil.users.get_user()
    if not user:
        raise Exception("No user is logged in")
    
    # Assuming 'datasets' is the table storing datasets with a 'user' column
    return app_tables.datasets.search(user=user)
