import geopy.distance
import googlemaps

class Address:

    def __init__(self, street_address, lat, long):
        self.streetAddress = street_address
        self.latitude = lat
        self.longitude = long

    def set_geo_location(self, lat, long):
        self.latitude = lat
        self.longitude = long

    def calc_distance(self, other_address):
        coord_self = (self.latitude, self.longitude)
        coord_other = (other_address.latitude, other_address.longitude)
        return geopy.distance.vincenty(coord_self, coord_other).km

    def get_google_geo_location(self):
        gmaps = googlemaps.Client(key="AIzaSyD9dY-YAShRckBdvKjbOT7yo2ebNCcwWWc")
        geocode_result = gmaps.geocode(self.streetAddress)
        self.latitude = geocode_result[0][u"geometry"][u"location"][u"lat"]
        self.longitude = geocode_result[0][u"geometry"][u"location"][u"lng"]
