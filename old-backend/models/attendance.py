import datetime
from google.cloud.firestore import GeoPoint


class Attendance:
    def __init__(
        self,
        date: datetime.date,
        user_id: str,
        user_name: str,
        check_in_at: datetime.datetime,
        commitment_time: str,
        ip_address: str,
        lat_lng: GeoPoint,
        place_name: str,
        time_difference_seconds: float,
    ):
        self.date = date
        self.user_id = user_id
        self.user_name = user_name
        self.check_in_at = check_in_at
        self.commitment_time = commitment_time
        self.ip_address = ip_address
        self.lat_lng = lat_lng
        self.place_name = place_name
        self.time_difference_seconds = time_difference_seconds

    def __repr__(self):
        return f"<Attendance(user_id={self.user_id}, user_name={self.user_name}, check_in_at={self.check_in_at}, commitment_time={self.commitment_time}, place_name={self.place_name}, time_difference_seconds={self.time_difference_seconds})>"
