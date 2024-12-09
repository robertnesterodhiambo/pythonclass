import bcrypt

def hash_password(password):
    """
    Hash the password using bcrypt.
    The password should be a string and will be encoded to bytes before hashing.
    """
    # Ensure the password is in bytes format
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed


def check_password(stored_hash, password):
    """
    Check if the password matches the stored hash.
    Both password and stored_hash need to be in bytes format.
    """
    # Ensure stored_hash is in bytes format
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
    
    # Ensure password is in bytes format
    if isinstance(password, str):
        password = password.encode('utf-8')  # Encode password to bytes if it's a string
    
    # Compare password to stored hash
    return bcrypt.checkpw(password, stored_hash)
