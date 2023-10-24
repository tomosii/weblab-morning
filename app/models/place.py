from google.cloud.firestore import GeoPoint


class Place:
    def __init__(self, name: str, ip_addresses: list[str], lat_lng: GeoPoint):
        self.name = name
        self.ip_addresses = ip_addresses
        self.lat_lng = lat_lng

    @staticmethod
    def from_dict(data: dict):
        return Place(
            name=data["name"],
            ip_addresses=data["ipAddresses"],
            lat_lng=data["latLng"],
        )

    def __str__(self):
        return f"Place(name={self.name}, ip_addresses={self.ip_addresses}, lat_lng={self.lat_lng})"
