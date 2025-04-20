from google.cloud.firestore import GeoPoint


class Place:
    def __init__(
        self,
        id: str,
        name: str,
        ip_addresses: list[str],
        lat_lng: GeoPoint,
        enabled: bool,
    ):
        self.id = id
        self.name = name
        self.ip_addresses = ip_addresses
        self.lat_lng = lat_lng
        self.enabled = enabled

    @staticmethod
    def from_dict(data: dict):
        return Place(
            id=data["id"],
            name=data["name"],
            ip_addresses=data["ipAddresses"],
            lat_lng=data["latLng"],
            enabled=data["enabled"],
        )

    def __repr__(self):
        return f"<Place(name={self.name}, ip_addresses={self.ip_addresses}, lat_lng={self.lat_lng}, enabled={self.enabled})>"
