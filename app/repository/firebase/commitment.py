from app.repository.firebase.firestore import db


class CommitmentRepository:
    def __init__(self):
        self.collection = db.collection("commitments")

    def put(self, user_id: str, user_name: str, time: str, day: str):
        doc_ref = self.collection.document(day)
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
                    "enabled": True,
                }
            }
        )
        print(f"[Firestore] Put commitment: {day}, {user_id}, {time}")

    def puts(self, user_id: str, user_name: str, time: str, days: list):
        for day in days:
            self.put(
                user_id=user_id,
                user_name=user_name,
                time=time,
                day=day,
            )

    def get(self, day: str):
        doc = self.collection.document(day).get()

        if not doc.exists:
            return {}

        return doc.to_dict()
