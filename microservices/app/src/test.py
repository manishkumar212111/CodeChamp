import hashing

password="man12345"
username= "SUPP_"+"manish7297"

a=hashing.hash_password(password)
print a
print username

result=[{"username":"SUPP_manish7297","password":"841ddade7f5daeb3c05403c3fd1bf0d3e23500a2d59f686283e27a7d12c4e24a:3fbeffca8e9b4f27b7adde3161aff3e8"}]

print result[0]['username']