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


class UserPoint:
    def __init__(
        self,
        user_id: str,
        user_name: str,
        dates: list[datetime.date],
        total_point: int,
        total_penalty: int,
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.dates = dates
        self.total_point = total_point
        self.total_penalty = total_penalty

    def __repr__(self):
        return f"<UserPoint {self.user_id} {self.user_name} {self.total_point} {self.total_penalty}>"


class UserWinningTimes:
    def __init__(
        self,
        user_id: str,
        user_name: str,
        winning_times: int,
        rewards: float,
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.winning_times = winning_times
        self.rewards = rewards

    def __repr__(self):
        return f"<UserWinningTimes {self.user_id} {self.user_name} {self.winning_times} {self.rewards}>"
