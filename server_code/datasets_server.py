import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import io
from tabulate import tabulate  # For text formatting
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




def clean_preview_data(df):
    """Clean the dataset for preview by handling missing values and mixed types."""
    df.fillna("N/A", inplace=True)  # Replace missing values with "N/A"
    for col in df.columns:
        if df[col].dtype == 'object':  # Check for mixed types
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except Exception as e:
                print(f"Error processing column {col}: {e}")
    return df

@anvil.server.callable
def generate_preview(file):
    """Generate a preview of the dataset."""
    try:
        if file.content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/json':
            df = pd.read_json(io.BytesIO(file.get_bytes()))
        else:
            return "Unsupported file type.", []

        # Clean the dataset
        df = clean_preview_data(df)

        # Format .describe() output
        describe_output = tabulate(df.describe(include="all"), headers="keys", tablefmt="grid")
        preview_rows = df.head(5).to_dict(orient="records")  # First 10 rows
        return describe_output, preview_rows
    except Exception as e:
        print(f"Error generating preview: {e}")
        return f"Error generating preview: {e}", []

@anvil.server.callable
def preview_dataset(dataset_id):
    """Generates a preview of the dataset stored in the Vault."""
    try:
        dataset_row = app_tables.datasets.get_by_id(dataset_id)
        if not dataset_row:
            return "Dataset not found.", []

        file = dataset_row['fulldataset']
        if not file:
            return "No file found.", []

        if file.content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/json':
            df = pd.read_json(io.BytesIO(file.get_bytes()))
        else:
            return "Unsupported file type.", []

        # Clean and format the dataset
        df = clean_preview_data(df)
        describe_output = tabulate(df.describe(include="all"), headers="keys", tablefmt="grid")
        preview_rows = df.head(10).to_dict(orient="records")
        return describe_output, preview_rows
    except Exception as e:
        print(f"Error previewing dataset: {e}")
        return f"Error previewing dataset: {e}", []

      
  
