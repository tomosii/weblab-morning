import datetime


class Point:
    def __init__(
        self,
        date: datetime.date,
        user_id: str,
        user_name: str,
        point: int,
        penalty: int,
    ):
        self.date = date
        self.user_id = user_id
        self.user_name = user_name
        self.point = point
        self.penalty = penalty

    def __repr__(self):
        return f"<Point(user_id={self.user_id}, user_name={self.user_name}, point={self.point}, penalty={self.penalty})>"
