import datetime

from app.repository.firebase.firestore import db
from app.models.point import Point


class PointRepository:
    def __init__(self):
        self.collection = db.collection("points")

    def get_point(self, date: datetime.date) -> list[Point]:
        doc_ref = self.collection.document(date.strftime("%Y-%m-%d"))
        doc = doc_ref.get()

        if not doc.exists:
            return []

        points = [
            Point(
                start_date=date,
                user_id=data["userId"],
                user_name=data["userName"],
                point=data["point"],
                penalty=data["penalty"],
            )
            for data in doc.to_dict().values()
        ]

        print(f"[Firestore] Get {len(points)} points of {date}")
        return points

    def put_point(
        self,
        start_date: datetime.date,
        user_id: str,
        user_name: str,
        point: int,
        penalty: int,
    ):
        doc_ref = self.collection.document(start_date.strftime("%Y-%m-%d"))
        doc = doc_ref.get()

        # Create empty document if not exists
        if not doc.exists:
            doc_ref.set({})

        doc_ref.update(
            {
                user_id: {
                    "userId": user_id,
                    "userName": user_name,
                    "point": point,
                    "penalty": penalty,
                }
            }
        )
        print(f"[Firestore] Put point: {user_id} {start_date} {point} {penalty}")
