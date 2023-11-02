import datetime

from app.repository.firebase.firestore import db
from app.models.point import Point, UserPoint


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

    def get_all_points_of_weeks(self) -> dict[datetime.date, list[Point]]:
        week_points = {}
        for doc in self.collection.stream():
            week_points[doc.id] = [
                Point(
                    start_date=datetime.datetime.strptime(doc.id, "%Y-%m-%d").date(),
                    user_id=data["userId"],
                    user_name=data["userName"],
                    point=data["point"],
                    penalty=data["penalty"],
                )
                for data in doc.to_dict().values()
            ]
        print(f"[Firestore] Get {len(week_points)} weeks points")
        return week_points

    def get_all_points(self) -> list[Point]:
        all_points = []
        for doc in self.collection.stream():
            all_points.extend(
                [
                    Point(
                        start_date=datetime.datetime.strptime(
                            doc.id, "%Y-%m-%d"
                        ).date(),
                        user_id=data["userId"],
                        user_name=data["userName"],
                        point=data["point"],
                        penalty=data["penalty"],
                    )
                    for data in doc.to_dict().values()
                ]
            )
        print(f"[Firestore] Get {len(all_points)} points")
        return all_points

    def get_all_user_points(self) -> list[UserPoint]:
        all_points = []
        for doc in self.collection.stream():
            all_points.extend(
                [
                    Point(
                        start_date=datetime.datetime.strptime(
                            doc.id, "%Y-%m-%d"
                        ).date(),
                        user_id=data["userId"],
                        user_name=data["userName"],
                        point=data["point"],
                        penalty=data["penalty"],
                    )
                    for data in doc.to_dict().values()
                ]
            )
        user_points = self.parse_user_points(all_points)
        return user_points

    @staticmethod
    def parse_user_points(points: list[Point]) -> list[UserPoint]:
        user_map: dict[str, UserPoint] = {}
        for point in points:
            if point.user_id not in user_map:
                user_map[point.user_id] = UserPoint(
                    user_id=point.user_id,
                    user_name=point.user_name,
                    dates=[point.start_date],
                    total_point=point.point,
                    total_penalty=point.penalty,
                )
            else:
                user_map[point.user_id].dates.append(point.start_date)
                user_map[point.user_id].total_point += point.point
                user_map[point.user_id].total_penalty += point.penalty
        user_points = list(user_map.values())
        return user_points

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
