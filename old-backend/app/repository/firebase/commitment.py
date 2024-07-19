import datetime

from app.repository.firebase.firestore import db
from app.models.commitment import Commitment, UserCommitment


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
                    "userId": user_id,
                    "userName": user_name,
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

    def get_commit(self, date: datetime.date) -> list[Commitment]:
        doc = self.collection.document(date.strftime("%Y-%m-%d")).get()
        if not doc.exists:
            return []

        commitments = []
        for user_id, data in doc.to_dict().items():
            if data["enabled"]:
                commitments.append(
                    Commitment(
                        date=date,
                        user_id=data["userId"],
                        user_name=data["userName"],
                        time=data["time"],
                    )
                )
        print(f"[Firestore] Get {len(commitments)} enabled commitments of {date}")
        return commitments

    def get_user_commits(self, dates: list[datetime.date]) -> list[UserCommitment]:
        commitments = []
        for date in dates:
            commit = self.get_commit(date=date)
            commitments.extend(commit)
        user_commits = self.parse_user_commitments(commits=commitments)
        return user_commits

    def get_all_user_commits(self) -> list[UserCommitment]:
        all_commits = []
        for doc in self.collection.stream():
            for user_id, data in doc.to_dict().items():
                if data["enabled"]:
                    all_commits.append(
                        Commitment(
                            date=datetime.datetime.strptime(doc.id, "%Y-%m-%d").date(),
                            user_id=data["userId"],
                            user_name=data["userName"],
                            time=data["time"],
                        )
                    )
        user_commits = self.parse_user_commitments(commits=all_commits)
        return user_commits

    @staticmethod
    def parse_user_commitments(commits: list[Commitment]) -> list[UserCommitment]:
        user_map: dict[str, UserCommitment] = {}
        for commit in commits:
            if commit.user_id not in user_map:
                user_map[commit.user_id] = UserCommitment(
                    user_id=commit.user_id,
                    user_name=commit.user_name,
                    time=commit.time,
                    dates=[commit.date],
                )
            else:
                user_map[commit.user_id].dates.append(commit.date)
        user_commits = list(user_map.values())
        print(f"Parsed {len(user_commits)} user commitments.")
        return user_commits
