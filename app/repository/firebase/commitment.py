import datetime

from app.repository.firebase.firestore import db


class CommitmentRepository:
    def __init__(self):
        self.collection = db.collection("commitments")

    def put_commit(
        self,
        user_id: str,
        user_name: str,
        time: str,
        date: datetime.date,
        enabled: bool = True,
    ):
        doc_ref = self.collection.document(date.strftime("%Y-%m-%d"))
        doc = doc_ref.get()

        # Create empty document if not exists
        if not doc.exists:
            doc_ref.set({})

        doc_ref.update(
            {
                user_id: {
                    "user_id": user_id,
                    "user_name": user_name,
                    "time": time,
                    "enabled": enabled,
                }
            }
        )
        print(f"[Firestore] Put commitment: {date}, {user_id}, {time}")

    def put_commits(
        self, user_id: str, user_name: str, time: str, dates: list[datetime.date]
    ):
        for date in dates:
            self.put_commit(
                user_id=user_id,
                user_name=user_name,
                time=time,
                date=date,
            )

    def disable_commit(self, user_id: str, date: datetime.date):
        doc_ref = self.collection.document(date.strftime("%Y-%m-%d"))
        doc = doc_ref.get()

        if not doc.exists:
            return

        doc_ref.update(
            {
                user_id: {
                    "enabled": False,
                }
            }
        )
        print(f"[Firestore] Disable commitment: {date}, {user_id}")

    def disable_commits(self, user_id: str, dates: list[datetime.date]):
        for date in dates:
            self.disable_commit(user_id=user_id, date=date)

    def get(self, date: str):
        doc = self.collection.document(date).get()

        if not doc.exists:
            return {}

        return doc.to_dict()
