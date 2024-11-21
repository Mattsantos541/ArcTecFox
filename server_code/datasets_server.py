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


@anvil.server.callable
def generate_preview(file):
    """Generate a preview of the dataset including .describe() and the first 5 rows."""
    try:

        # Load the dataset into a DataFrame depending on file type
        if file.content_type == 'text/csv':
            df = pd.read_csv(file.get_bytes_io())
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file.get_bytes_io())
        elif file.content_type == 'application/json':
            df = pd.read_json(file.get_bytes_io())
        else:
            return "Unsupported file type.", []

        # Generate .describe() output as a string
        describe_output = df.describe(include='all').to_string()  # Include all columns

        # Extract the first 5 rows for preview
        preview_rows = df.head().to_dict(orient='records')
        return describe_output, preview_rows
    except Exception as e:
        print(f"Error generating preview: {str(e)}")
        return f"Error generating preview: {str(e)}", []


@anvil.server.callable
def preview_dataset(dataset_id):
    """Generates a preview of the dataset stored in the Vault by dataset ID."""
    import pandas as pd
    import io

    # Fetch the dataset row by its ID
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

        # Generate .describe() output as a string
        describe_output = df.describe(include='all').to_string()  # Include all columns

        # Extract the first 5 rows for preview
        preview_rows = df.head().to_dict(orient='records')

        return describe_output, preview_rows
    except Exception as e:
        print(f"Error generating preview: {str(e)}")
        return f"Error generating preview: {str(e)}", []
