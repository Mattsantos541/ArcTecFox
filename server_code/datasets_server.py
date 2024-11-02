import anvil.users
import anvil.tables as tables
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

@anvil.server.callable
def upload_dataset(file, description):
  """Uploads a dataset to the datasets table"""
  user = anvil.users.get_user()
  if not user:
    raise anvil.users.AuthenticationFailed("User must be logged in to upload a dataset")

  try:
  # # # Determine file type and read data accordingly
  # #   if file.content_type == 'text/csv':
  # #     df = pd.read_csv(io.BytesIO(file.get_bytes()))
  # #   elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
  # #     df = pd.read_excel(io.BytesIO(file.get_bytes()))
  # #   elif file.content_type == 'application/json':
  # #     df = pd.read_json(io.BytesIO(file.get_bytes()))
  # #   else:
  # #     return "Unsupported file type."

  # # # Count the number of rows in the dataset
  # #   row_count = len(df)

  # #       # Store dataset information in the datasets table
  #   app_tables.datasets.add_row(
    user=user,
    dataset_name=file.name,
    description=description,
    upload_date=datetime.now(),
    fulldataset=file,  # Save the original file in the Media column
    size=row_count
    )
        
    return "success"
  except Exception as e:
        print(f"Error uploading dataset: {str(e)}")
        return "failure"

@anvil.server.callable
def preview_dataset(dataset_id):
    """Generates a preview of the dataset stored in the datasets table by ID"""
    dataset_row = app_tables.datasets.get_by_id(dataset_id)
    if not dataset_row:
        return "Dataset not found.", []

    file = dataset_row['fulldataset']
    if not file:
        return "No file found in this dataset.", []

    try:
        # Read the file based on its type and generate a preview
        if file.content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/json':
            df = pd.read_json(io.BytesIO(file.get_bytes()))
        else:
            return "Unsupported file type.", []

        # Generate preview information and first 5 rows
        preview_info = df.info(buf=io.StringIO()).getvalue()  # Basic info as a string
        preview_rows = df.head().to_dict(orient='records')    # First 5 rows as a list of dictionaries

        return preview_info, preview_rows
    except Exception as e:
        print(f"Error generating preview: {str(e)}")
        return f"Error generating preview: {str(e)}", []

@anvil.server.callable
def fetch_vault_datasets():
    """Fetch datasets stored in the Vault for the current user."""
    user = anvil.users.get_user()
    if not user:
        raise anvil.users.AuthenticationFailed("User must be logged in to access datasets")
    
    return app_tables.datasets.search(user=user)

@anvil.server.callable
def preview_dataset(dataset_id):
    """Generates a preview of the dataset stored in the Vault by dataset ID."""
    dataset_row = app_tables.datasets.get_by_id(dataset_id)
    if not dataset_row:
        return "Dataset not found.", []

    file = dataset_row['fulldataset']
    if not file:
        return "No file found in this dataset.", []

    try:
        # Read the file based on its content type
        if file.content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/json':
            df = pd.read_json(io.BytesIO(file.get_bytes()))
        else:
            return "Unsupported file type.", []

        # Generate basic info and first 5 rows for preview
        preview_info = df.info(buf=io.StringIO()).getvalue()  # Basic info as string
        preview_rows = df.head().to_dict(orient='records')    # First 5 rows as list of dicts

        return preview_info, preview_rows
    except Exception as e:
        print(f"Error generating preview: {str(e)}")
        return f"Error generating preview: {str(e)}", []