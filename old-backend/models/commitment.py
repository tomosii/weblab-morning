import datetime


class Commitment:
    def __init__(self, date: datetime.date, user_id: str, user_name: str, time: str):
        self.date = date
        self.user_id = user_id
        self.user_name = user_name
        self.time = time

    def __str__(self):
        return f"Commitment(date={self.date}, user_id={self.user_id}, user_name={self.user_name}, time={self.time})"


class UserCommitment:
    def __init__(
        self, user_id: str, user_name: str, time: str, dates: list[datetime.date]
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.time = time
        self.dates = dates

    def __repr__(self):
        return f"UserCommitment(user_id={self.user_id}, user_name={self.user_name}, time={self.time}, dates={self.dates})"
