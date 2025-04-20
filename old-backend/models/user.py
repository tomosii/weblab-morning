class User:
    def __init__(
        self,
        id: str,
        email: str,
        nickname: str,
    ):
        self.id = id
        self.email = email
        self.nickname = nickname

    @staticmethod
    def from_dict(data: dict):
        return User(
            id=data["id"],
            email=data["email"],
            nickname=data["nickname"],
        )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, nickname={self.nickname})>"
