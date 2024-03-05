import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from argon2 import PasswordHasher

ph = PasswordHasher()

@anvil.server.callable
def register_user(email, password, confirm_password, business_name):
    if password != confirm_password:
        raise ValueError("Passwords do not match")
    
    if app_tables.users.get(email=email):
        raise ValueError("Email is already in use")
    
    if not business_name:
        business_name = "Personal"
    
    password_hash = ph.hash(password)
    
    new_user = app_tables.users.add_row(email=email,
                                        password_hash=password_hash,
                                        business_name=business_name,
                                        confirmed=False)
    
    # Generate a unique token for email confirmation, e.g., a UUID
    confirmation_token = anvil.server.generate_uuid()
    # You might want to store this token in the database associated with the user for later verification
    
    # Send confirmation email
    confirmation_url = f"{anvil.server.get_app_origin()}/#/confirm_email?token={confirmation_token}"
    anvil.email.send(to=email,
                     subject="Confirm your email",
                     text=f"Please confirm your email by clicking on this link: {confirmation_url}")
    
    return "You have been successfully registered on ArcTecFox"