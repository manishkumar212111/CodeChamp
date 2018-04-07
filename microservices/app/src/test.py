from geopy.geocoders import GoogleV3
geocoder = GoogleV3()
location_list = geocoder.reverse((21.1673500,72.7850900))
location = location_list[0]
address = location.address
print address

