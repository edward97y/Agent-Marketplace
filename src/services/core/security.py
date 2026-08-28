from pwdlib import PasswordHash

password_hashing=PasswordHash.recommended()

def plan_to_hash_password(password:str)->str:
    return password_hashing.hash(password=password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hashing.verify(password=plain_password,hash=hashed_password)