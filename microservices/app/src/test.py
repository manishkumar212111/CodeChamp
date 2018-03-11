import bz2
password = "manish"
encrypted_password = bz2.compress(password)

print bz2.decompress(encrypted_password)
