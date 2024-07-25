import datetime

from google.cloud.firestore import GeoPoint

from .firestore import db
from ...models.attendance import Attendance


class AttendanceRepository:
    def __init__(self):
        self.collection = db.collection("attendances")

    def get_attendance(self, date: datetime.date) -> list[Attendance]:
        doc_ref = self.collection.document(date.strftime("%Y-%m-%d"))
        doc = doc_ref.get()

        if not doc.exists:
            return []

        attendances = [
            Attendance(
                date=date,
                user_id=data["userId"],
                user_name=data["userName"],
                check_in_at=data["checkInAt"],
                commitment_time=data["commitmentTime"],
                ip_address=data["ipAddress"],
                lat_lng=data["latLng"],
                place_name=data["placeName"],
                time_difference_seconds=data["timeDifferenceSeconds"],
            )
            for data in doc.to_dict().values()
        ]

        print(f"[Firestore] Get {len(attendances)} attendances of {date}")
        return attendances

    def get_attendances(self, dates: list[datetime.date]) -> list[Attendance]:
        attendances = []
        for date in dates:
            attendances.extend(self.get_attendance(date))
        return attendances

    def put_attendance(
        self,
        user_id: str,
        user_name: str,
        checkin_at: datetime.datetime,
        commitment_time: str,
        ip_address: str,
        latitude: float,
        longitude: float,
        place_name: str,
        time_difference_seconds: float,
    ):
        doc_ref = self.collection.document(checkin_at.strftime("%Y-%m-%d"))
        doc = doc_ref.get()

        # Create empty document if not exists
        if not doc.exists:
            doc_ref.set({})

        doc_ref.update(
            {
                user_id: {
                    "userId": user_id,
                    "userName": user_name,
                    "checkInAt": checkin_at,
                    "commitmentTime": commitment_time,
                    "ipAddress": ip_address,
                    "latLng": GeoPoint(latitude, longitude),
                    "placeName": place_name,
                    "timeDifferenceSeconds": time_difference_seconds,
                }
            }
        )
        print(f"[Firestore] Put attendance: {checkin_at}, {user_id}")
