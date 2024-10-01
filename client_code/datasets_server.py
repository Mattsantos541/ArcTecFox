import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

@anvil.server.callable
def get_vault_datasets():
    """Fetch datasets stored in the Vault"""
    return app_tables.datasets.search()

@anvil.server.callable
def preview_vault_dataset(dataset_id):
    """Preview the dataset stored in the Vault"""
    dataset = app_tables.datasets.get_by_id(dataset_id)
    file = dataset['fulldataset']
    
    # Here you call the preview generation logic
    return generate_preview(file)

@anvil.server.callable
def generate_preview(file):
    """Generate a preview of the dataset (pandas logic)"""
    import pandas as pd
    import io
    
    try:
        if file.content_type == 'text/csv':
            df = pd.read_csv(file.get_bytes_io())
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file.get_bytes_io())
        elif file.content_type == 'application/json':
            df = pd.read_json(file.get_bytes_io())
        else:
            return "Unsupported file type.", []

        # Get basic info about the dataset
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_output = buffer.getvalue()

        # Preview the first 5 rows of the dataset
        preview_rows = df.head().to_dict(orient='records')
        return info_output, preview_rows
    except Exception as e:
        return f"Error: {str(e)}", []
