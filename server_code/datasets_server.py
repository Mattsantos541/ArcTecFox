import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import io
from datetime import datetime  # Add datetime import

# Fetch datasets available to the current user
@anvil.server.callable
def get_user_vault_datasets():
    user = anvil.users.get_user()
    if not user:
        raise Exception("No user is logged in")
    return app_tables.datasets.search(user=user)

# Upload a dataset
@anvil.server.callable
def upload_dataset(file, description):
    user = anvil.users.get_user()
    if not user:
        raise anvil.users.AuthenticationFailed("User must be logged in to upload a dataset")

    try:
        # Determine file type and read data for row count
        if file.content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/json':
            df = pd.read_json(io.BytesIO(file.get_bytes()))
        else:
            return "Unsupported file type."

        row_count = len(df)

        # Store dataset information in the table
        app_tables.datasets.add_row(
            user=user,
            dataset_name=file.name,
            description=description,
            upload_date=datetime.now(),
            fulldataset=file,
            size=row_count
        )
        
        return "success"
    except Exception as e:
        print(f"Error uploading dataset: {str(e)}")
        return "failure"

# Generate a preview of a file's data
@anvil.server.callable
def generate_preview(file):
    try:
        if file.content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/json':
            df = pd.read_json(io.BytesIO(file.get_bytes()))
        else:
            return "Unsupported file type.", []

        # Generate pandas info and preview rows
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_output = buffer.getvalue()
        preview_rows = df.head().to_dict(orient='records')
        return info_output, preview_rows
    except Exception as e:
        print(f"Error generating preview: {str(e)}")
        return f"Error generating preview: {str(e)}", []

# Fetch a dataset for preview by its ID
@anvil.server.callable
def preview_dataset(dataset_id):
    dataset_row = app_tables.datasets.get_by_id(dataset_id)
    if not dataset_row:
        return "Dataset not found.", []

    file = dataset_row['fulldataset']
    if not file:
        return "No file found in this dataset.", []

    # Use the same `generate_preview` function to create the preview
    return generate_preview(file)
