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
  

def clean_preview_data(df, max_columns=5):
    """
    Clean the dataset to handle mixed data types, missing values, and column limits.
    """
    df.fillna("N/A", inplace=True)  # Replace missing values with a placeholder

    # Convert columns with mixed data types to strings
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')  # Convert to numeric where possible
            except Exception as e:
                print(f"Error processing column {col}: {e}")
        elif not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].astype(str)  # Convert non-numeric columns to strings

    # Limit the number of columns to max_columns
    if len(df.columns) > max_columns:
        df = df.iloc[:, :max_columns]

    return df

@anvil.server.callable
def generate_preview(file, max_columns=5):
    """
    Generate a preview of the dataset, showing a limited number of columns and rows.
    """
    try:
        # Load the dataset based on file type
        if file.content_type == 'text/csv':
            df = pd.read_csv(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(io.BytesIO(file.get_bytes()))
        elif file.content_type == 'application/json':
            df = pd.read_json(io.BytesIO(file.get_bytes()))
        else:
            return "Unsupported file type.", "No rows to display."

        # Clean and limit the dataset
        df = clean_preview_data(df, max_columns=max_columns)

        # Generate .describe() for numerical columns only
        numeric_cols = df.select_dtypes(include='number')
        if not numeric_cols.empty:
            describe_output = tabulate(numeric_cols.describe(), headers="keys", tablefmt="grid")
        else:
            describe_output = "No numeric columns available for summary."

        # Generate a preview of the first 10 rows (cleaned and truncated)
        head_output = tabulate(df.head(10), headers="keys", tablefmt="grid")

        return describe_output, head_output
    except Exception as e:
        print(f"Error generating preview: {e}")
        return f"Error generating preview: {e}", "No rows to display."


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

      
  
