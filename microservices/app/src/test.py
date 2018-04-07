from geopy.geocoders import GoogleV3
geocoder = GoogleV3()
location_list = geocoder.reverse((51.098989, 13.234234))
location = location_list[0]
address = location.address
print address

res=[{"department":"Municipal Corporation"}]

print res[0]['department']