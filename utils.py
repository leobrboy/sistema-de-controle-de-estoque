import bcrypt

def criptografar_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha_digitada, senha_hash):
    return bcrypt.checkpw(senha_digitada.encode(), senha_hash.encode())
