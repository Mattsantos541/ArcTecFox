import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import bcrypt

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

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
