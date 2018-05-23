from Address import Address
from firebase_admin import db


def get_address_firebase():
    return db.reference('addresses')


def get_all_database_address():
    ref = get_address_firebase()
    database_addresses = ref.get()
    addresses = []
    for key, value in database_addresses.items():
        a = Address(value['streetAddress'], value['lat'], value['long'])
        a.firebasekey = key
        addresses.append(a)
    return addresses


def update_all_database_addresses():
    ref = get_address_firebase()
    addresses = ref.get()
    for key, value in addresses.items():
        a = Address(value['streetAddress'], 0, 0)
        a.get_google_geo_location()
        cur_address_db = ref.child(key)
        cur_address_db.update({
            'lat': a.latitude,
            'long': a.longitude
        })


def add_address_to_database(address):
    ref = get_address_firebase()
    ref.push({
        'streetAddress': address.streetAddress,
        'lat': address.latitude,
        'long': address.longitude
    })


def get_addresses_within_location(street_address, dist_limit):
    comp_addr = Address(street_address, 0, 0)
    comp_addr.get_google_geo_location()
    addresses = get_all_database_address()
    addr_within_limit = []
    for address in addresses:
        dist = float(comp_addr.calc_distance(address))
        if dist < float(dist_limit):
            address.dist = dist
            addr_within_limit.append(address)
    addr_within_limit = sorted(addr_within_limit, key=lambda addr: addr.dist)
    return addr_within_limit


def remove_address_from_database(key):
    ref = get_address_firebase()
    ref.child(key).delete()


