import datetime


class Point:
    def __init__(
        self,
        start_date: datetime.date,
        user_id: str,
        user_name: str,
        point: int,
        penalty: int,
    ):
        self.start_date = start_date
        self.user_id = user_id
        self.user_name = user_name
        self.point = point
        self.penalty = penalty

    def __repr__(self):
        return f"<Point {self.start_date} {self.user_id} {self.point} {self.penalty}>"
