import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import bcrypt
import io
import pandas as pd

@anvil.server.callable
def register_user(email, password, confirm_password, business_name=None):
    # Validate the input data
    if not email or not password:
        raise ValueError("Email and password are required.")
    
    if password != confirm_password:
        raise ValueError("Passwords do not match.")
    
    # Check if the email is already in use
    if app_tables.users.get(email=email):
        raise ValueError("This email is already registered.")
    
    # Hash the password for security
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Store the new user in the "users" table
    app_tables.users.add_row(
        email=email,
        password=hashed_password,
        business_name=business_name,
        date_registered=anvil.server.now()
    )
    
    return "User registered successfully."

def check_user():
  if anvil.users.get_user() is None:
    raise anvil.server.NoUserError("No user is logged in.")


def get_user_datasets():
  #Retrieves datasets for the currently logged in user, returns list of datasets
  #first check if the user is logged in
  check_user()
  #fetch the datasets for the logged in user 
  user = anvil.users.get_user()
  return app_tables.datasets.search(user=user)

