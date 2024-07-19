import datetime

from app.repository.firebase.firestore import db


class TriviaRepository:
    def __init__(self):
        self.collection = db.collection("trivia")

    def put_trivia(
        self,
        user_id: str,
        user_name: str,
        trivia_text: str,
        created_at: datetime.datetime,
    ):
        # 自動IDでドキュメントを作成
        doc_ref = self.collection.document()
        doc_ref.set(
            {
                "userId": user_id,
                "userName": user_name,
                "text": trivia_text,
                "createdAt": created_at,
            }
        )
        print(f"[Firestore] Put trivia: {trivia_text}")
