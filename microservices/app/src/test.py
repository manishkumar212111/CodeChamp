'''from geopy.geocoders import GoogleV3
geocoder = GoogleV3()
location_list = geocoder.reverse((21.1673500,72.7850900))
location = location_list[0]
address = location.address
print address
'''
result=[
    {
        "p_id": 5,
        "latitude": "21.92000007629394",
        "longitude": "82.77999877929686",
        "im_id": "b1f18bf2-389d-491e-b72c-6c2af3f063db",
        "date": "2018-04-07"
    },
    {
        "p_id": 6,
        "latitude": "21.92000007629394",
        "longitude": "82.77999877929686",
        "im_id": "1e7edf3b-7a17-4f94-9590-ee0f196ba629",
        "date": "2018-04-07"
    },
    {
        "p_id": 7,
        "latitude": "21.92000007629394",
        "longitude": "82.77999877929686",
        "im_id": "1e7edf3b-7a17-4f94-9590-ee0f196ba629",
        "date": "2018-04-07"
    }
]
print result[1]