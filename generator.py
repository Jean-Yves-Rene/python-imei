import bcrypt
hashed_password = bcrypt.hashpw("GoogleISR2024?".encode('utf-8'), bcrypt.gensalt())
print(hashed_password.decode('utf-8'))
