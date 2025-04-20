from .firestore import db
from models.user import User


class UserRepository:
    def __init__(self):
        self.collection = db.collection("users")

    def get_user(self, email: str) -> User:
        doc = self.collection.document(email).get()
        if not doc.exists:
            print(f"[Firestore] User not found: {email}")
            return None
        user = User.from_dict(doc.to_dict())
        print(f"[Firestore] Get user: {user}")
        return user
